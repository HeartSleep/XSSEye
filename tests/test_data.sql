INSERT INTO xsseye.payloads(public_id, id_owner) VALUES ('asd', 1), ('qwe', 1);
INSERT INTO xsseye.reports
    (id_payload, protocol, hostname, port, path, client_ip, user_agent)
VALUES
    (1, 'https', 'test.cc', '443', '/', '10.10.10.10', 'testqwe123'),
    (1, 'https', 'asdqwe123.cc', '443', '/testazz', '10.10.10.10', 'testqwe123'),
    (1, 'https', 'asdqwe123.cc', '443', '/a', '10.10.10.10', 'testqwe123'),
    (1, 'https', 'asdqwe123.cc', '443', '/b', '10.10.10.10', 'testqwe123'),
    (1, 'https', 'asdqwe123.cc', '443', '/c', '10.10.10.10', 'testqwe123'),
    (1, 'https', 'asdqwe123.cc', '443', '/d', '10.10.10.10', 'testqwe123'),
    (1, 'https', 'asdqwe123.cc', '443', '/h4rd_find', '10.10.10.10', 'testqwe123'),
    (2, 'https', 'example.com', '80', '/', '10.10.10.10', 'testqwe123'),
    (2, 'https', 'example.com', '8080', '/', '10.10.10.10', 'testqwe123');

-- ADVANCED INSERT
INSERT INTO xsseye.reports
    (id_payload, protocol, hostname, port, path, client_ip, user_agent, query, hash, cookies)
VALUES
    (1, 'https', 'test1.cc', '443', '/', '10.10.10.10', 'testqwe123', 'testqery=test&test%20=tset', 'testHash', '{"testcookie": "value"}'::json),
    (1, 'https', 'test2.cc', '443', '/testazz', '10.10.10.10', 'testqwe123', 'testqery=test&test%20=tset', '1337', '{"testcookie111": "value"}'::json);