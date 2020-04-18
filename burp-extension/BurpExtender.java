package burp;

import org.apache.commons.lang3.SystemUtils;
import org.apache.http.NameValuePair;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;

import javax.swing.*;

import java.io.*;
import java.util.*;
import java.lang.System;
import java.nio.file.*;

import org.json.*;

class Config {
    public static Path configFilepath = null;
    public static String apiUrl = "";
    public static String username = "";
    public static String password = "";

    public static Path getConfigPath() {
        if (configFilepath != null)
            return configFilepath;
        Path configDir = null;
        if (SystemUtils.IS_OS_WINDOWS) {
            String appData = System.getenv("APPDATA");
            if (appData != null) {
                configDir = Paths.get(appData);
            } else {
                configDir = Paths.get(System.getProperty("user.home"), "AppData", "Roaming");
            }
        } else if (SystemUtils.IS_OS_UNIX) {
            configDir = Paths.get(System.getProperty("user.home"));
        }
        Config.configFilepath = configDir.resolve("xsseye.config.json").normalize();
        BurpExtender.stdout.println("Config path: " + Config.configFilepath.toString());
        if (!Files.exists(Config.configFilepath)) {
            BurpExtender.stdout.println("Config file not found. Try to write default config.");
            String defaultConfig = "{\n" +
                    "\t\"api_url\": \"https://l0r.ru/api/payloads/get_url\",\n" +
                    "\t\"username\": \"\",\n" +
                    "\t\"password\": \"\"\n" +
                    "}";
            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter(Config.configFilepath.toString()));
                writer.write(defaultConfig);
                writer.close();
                BurpExtender.stdout.println("Default config written in " + Config.configFilepath);
            } catch (Exception e) {
                e.printStackTrace(BurpExtender.stderr);
            }
        }
        return configFilepath;
    }

    public static void loadConfig() {
        if (Config.configFilepath == null)
            Config.getConfigPath();
        try {
            JSONObject jsonObject = new JSONObject(new String(Files.readAllBytes(Config.configFilepath)));
            Config.apiUrl = jsonObject.getString("api_url");
            Config.username = jsonObject.getString("username");
            Config.password = jsonObject.getString("password");
        } catch (Exception e) {
            e.printStackTrace(BurpExtender.stderr);
        }
    }
}

class PayloadStream extends FilterInputStream {
    /*
     * System vars
     */
    final String hostname, protocol;
    final int port;
    final byte[] search, request;


    private byte[] getPayloadURL(String host, int port, String protocol, byte[] request) {
        Config.loadConfig();
        try {
            HttpPost post = new HttpPost(Config.apiUrl);

            RequestConfig.Builder requestConfig = RequestConfig.custom();
            requestConfig.setConnectTimeout(3 * 1000);
            requestConfig.setConnectionRequestTimeout(3 * 1000);
            requestConfig.setSocketTimeout(3 * 1000);

            post.setConfig(requestConfig.build());

            List<NameValuePair> urlParameters = new ArrayList<>();
            urlParameters.add(new BasicNameValuePair("hostname", host));
            urlParameters.add(new BasicNameValuePair("port", String.valueOf(port)));
            urlParameters.add(new BasicNameValuePair("protocol", protocol));
            urlParameters.add(new BasicNameValuePair("request_base64", new String(Base64.getEncoder().encode(request))));
            urlParameters.add(new BasicNameValuePair("_username", Config.username));
            urlParameters.add(new BasicNameValuePair("_password", Config.password));

            post.setEntity(new UrlEncodedFormEntity(urlParameters));

            try (CloseableHttpClient httpClient = HttpClients.createDefault();
                 CloseableHttpResponse response = httpClient.execute(post)) {
                if (response.getStatusLine().getStatusCode() != 200) {
                    throw new Exception("Invalid request. Server returned " + response.getStatusLine().toString());
                }
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                response.getEntity().writeTo(baos);
                return baos.toByteArray();
            }
        } catch (Exception e) {
            e.printStackTrace(BurpExtender.stderr);
            JOptionPane.showMessageDialog(null, "Cann't get payload url. Payload will not been replaced!\n" +
                    "You can find additional info about error in Burp Extender tab.", "XSSEye Error!", JOptionPane.ERROR_MESSAGE);

            return null;
        }
    }

    LinkedList<Integer> inQueue = new LinkedList<Integer>();
    LinkedList<Integer> outQueue = new LinkedList<Integer>();

    protected PayloadStream(InputStream in,
                            byte[] search,
                            String hostname, int port, String protocol,
                            byte[] request) {
        super(in);
        this.search = search;
        this.hostname = hostname;
        this.port = port;
        this.protocol = protocol;
        this.request = request;
    }

    private boolean isMatchFound() {
        Iterator<Integer> inIter = inQueue.iterator();
        for (int i = 0; i < search.length; i++) // TODO WRITE TESTS!!! LowerCase can not work on special chars
            if (!inIter.hasNext() || Character.toLowerCase(search[i]) != Character.toLowerCase(inIter.next()))
                return false;
        return true;
    }

    @Override
    public int read() throws IOException {
        if (outQueue.isEmpty()) {
            while (inQueue.size() < search.length) {
                int next = super.read();
                inQueue.offer(next);
                if (next == -1)
                    break;
            }

            if (isMatchFound()) {
                byte[] payloadUrl = getPayloadURL(
                        hostname,
                        port,
                        protocol,
                        request
                );
                if (payloadUrl != null) {
                    BurpExtender.stdout.println("Got a Payload URL: " + new String(payloadUrl));
                    for (int i = 0; i < search.length; i++)
                        inQueue.remove();

                    for (byte b : payloadUrl)
                        outQueue.offer((int) b);
                } else {
                    outQueue.add(inQueue.remove());
                    BurpExtender.stdout.println("Error trying to get payload url");
                }
            } else {
                outQueue.add(inQueue.remove());
            }
        }

        return outQueue.remove();
    }
}


public class BurpExtender implements IBurpExtender, IHttpListener {
    public static IBurpExtenderCallbacks callbacks;
    public static PrintWriter stdout, stderr;


    @Override
    public void registerExtenderCallbacks(IBurpExtenderCallbacks callbacks) {
        this.stdout = new PrintWriter(callbacks.getStdout(), true);
        this.stderr = new PrintWriter(callbacks.getStderr(), true);
        this.callbacks = callbacks;
        callbacks.setExtensionName("XSSEye Burp Extension");
        Config.loadConfig();
        callbacks.registerHttpListener((IHttpListener) this);

    }

    @Override
    public void processHttpMessage(int toolFlag, boolean messageIsRequest, IHttpRequestResponse messageInfo) {
        // Only accept Proxy Meesage (4)
        //if (messageIsRequest && toolFlag == 4) {
        if (messageIsRequest) {
            byte[] request = messageInfo.getRequest();
            byte[] search = "{XSSEYE_URL}".getBytes();
            IHttpService httpService = messageInfo.getHttpService();

            ByteArrayInputStream bis = new ByteArrayInputStream(request);

            InputStream ris = new PayloadStream(
                    bis, search,
                    httpService.getHost(), httpService.getPort(), httpService.getProtocol(),
                    request
            );

            ByteArrayOutputStream bos = new ByteArrayOutputStream();

            int b;
            try {
                while (-1 != (b = ris.read()))
                    bos.write(b);

                messageInfo.setRequest(bos.toByteArray());
            } catch (Exception e) {
                e.printStackTrace(this.stderr);
            }
        }
    }

}