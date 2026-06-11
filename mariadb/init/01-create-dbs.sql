CREATE DATABASE IF NOT EXISTS bookstack CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'bookstack_user'@'%' IDENTIFIED BY 'bookstack8432';

GRANT ALL PRIVILEGES ON bookstack.* TO 'bookstack_user'@'%';

FLUSH PRIVILEGES;