-- Create users_user table
CREATE TABLE IF NOT EXISTS "users_user" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "password" varchar(128) NOT NULL,
    "last_login" timestamp with time zone NULL,
    "is_superuser" boolean NOT NULL,
    "username" varchar(150) NOT NULL UNIQUE,
    "first_name" varchar(150) NOT NULL,
    "last_name" varchar(150) NOT NULL,
    "email" varchar(254) NULL,
    "is_staff" boolean NOT NULL,
    "is_active" boolean NOT NULL,
    "date_joined" timestamp with time zone NOT NULL,
    "phone" varchar(20) NOT NULL UNIQUE,
    "address" text NULL,
    "is_customer" boolean NOT NULL,
    "is_staff_member" boolean NOT NULL
);

-- Create products_category table
CREATE TABLE IF NOT EXISTS "products_category" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "description" text NULL,
    "image" varchar(100) NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);

-- Create products_product table
CREATE TABLE IF NOT EXISTS "products_product" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL,
    "description" text NOT NULL,
    "price" decimal(10, 2) NOT NULL,
    "image" varchar(100) NOT NULL,
    "stock" integer NOT NULL,
    "is_active" boolean NOT NULL,
    "is_featured" boolean NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL,
    "category_id" bigint NOT NULL REFERENCES "products_category" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Create orders_order table
CREATE TABLE IF NOT EXISTS "orders_order" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "order_number" varchar(50) NOT NULL UNIQUE,
    "status" varchar(20) NOT NULL,
    "total_amount" decimal(10, 2) NOT NULL,
    "shipping_address" text NOT NULL,
    "notes" text NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL,
    "user_id" bigint NOT NULL REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Create orders_orderitem table
CREATE TABLE IF NOT EXISTS "orders_orderitem" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "quantity" integer NOT NULL,
    "price" decimal(10, 2) NOT NULL,
    "order_id" bigint NOT NULL REFERENCES "orders_order" ("id") DEFERRABLE INITIALLY DEFERRED,
    "product_id" bigint NOT NULL REFERENCES "products_product" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Create notifications_notification table
CREATE TABLE IF NOT EXISTS "notifications_notification" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "title" varchar(200) NOT NULL,
    "message" text NOT NULL,
    "is_read" boolean NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "user_id" bigint NOT NULL REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Create test_app_testmodel table
CREATE TABLE IF NOT EXISTS "test_app_testmodel" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);

-- Create admin user
INSERT INTO users_user (password, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, phone, is_customer, is_staff_member)
VALUES ('pbkdf2_sha256$600000$abcdefghijklmnopqrstuvwxABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$abcdefghijklmnopqrstuvwxABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 
true, 'admin', 'Admin', 'User', true, true, NOW(), '07123456789', false, true);

-- Create sample category
INSERT INTO products_category (name, created_at, updated_at)
VALUES ('أجهزة إلكترونية', NOW(), NOW());

-- Create sample product
INSERT INTO products_product (name, description, price, image, stock, is_active, is_featured, created_at, updated_at, category_id)
VALUES ('هاتف ذكي', 'هاتف ذكي بمواصفات عالية', 500.00, 'products/sample.jpg', 10, true, true, NOW(), NOW(), 1);
