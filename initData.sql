--初始化数据库版本
INSERT INTO dbupdate (key, value) VALUES ('version', 'ver0.006');

--初始化role
INSERT INTO role (id, name) VALUES (0, '游客');
INSERT INTO role (id, name) VALUES (1, '站长');
INSERT INTO role (id, name) VALUES (2, '管理员');
INSERT INTO role (id, name) VALUES (3, '会员');

--初始化right
INSERT INTO right (id, name) VALUES (0, '管理管理员账户');
INSERT INTO right (id, name) VALUES (1, '管理会员账户');
INSERT INTO right (id, name) VALUES (2, '管理比赛');
INSERT INTO right (id, name) VALUES (3, '上传比赛记录');
INSERT INTO right (id, name) VALUES (4, '发表评论');

--初始化各role拥有的right
--游客 无权利
--站长 拥有所有权限
INSERT INTO roleRight (id_role, id_right) VALUES (1, 0);
INSERT INTO roleRight (id_role, id_right) VALUES (1, 1);
INSERT INTO roleRight (id_role, id_right) VALUES (1, 2);
INSERT INTO roleRight (id_role, id_right) VALUES (1, 3);
INSERT INTO roleRight (id_role, id_right) VALUES (1, 4);
--管理员 拥有除了0以外的权限
INSERT INTO roleRight (id_role, id_right) VALUES (2, 1);
INSERT INTO roleRight (id_role, id_right) VALUES (2, 2);
INSERT INTO roleRight (id_role, id_right) VALUES (2, 3);
INSERT INTO roleRight (id_role, id_right) VALUES (2, 4);
--会员 上传记录和发表评论的权限
INSERT INTO roleRight (id_role, id_right) VALUES (3, 3);
INSERT INTO roleRight (id_role, id_right) VALUES (3, 4);

--username: admin
--password: admin        (while salt is rnd495)
INSERT INTO user (username, password, id_role, des) 
VALUES (
    'admin', 
    '916b08734c2c8295b523b4f7d95821b3726d9dc13b9e31f889808d41486e5d64',
    1,
    'administrator');

--初始化gameStatu
INSERT INTO gameStatu (id, name) VALUES (0, '准备中');
INSERT INTO gameStatu (id, name) VALUES (1, '已开始');
INSERT INTO gameStatu (id, name) VALUES (2, '已结束');

--初始化teamRole
INSERT INTO teamRole (id, name) VALUES (0, '队长');
INSERT INTO teamRole (id, name) VALUES (1, '队员');
INSERT INTO teamRole (id, name) VALUES (2, '替补');
INSERT INTO teamRole (id, name) VALUES (3, '空位');