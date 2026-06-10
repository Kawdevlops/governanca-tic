CREATE DATABASE IF NOT EXISTS bookstack2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'bookstack_user'@'%' IDENTIFIED BY 'bookstack8432';

GRANT ALL PRIVILEGES ON bookstack2.* TO 'bookstack_user'@'%';

FLUSH PRIVILEGES;