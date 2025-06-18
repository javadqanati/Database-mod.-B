FROM php:8.2-apache

RUN a2enmod rewrite

RUN apt-get update && apt-get install -y \
    libzip-dev zip unzip git libpng-dev libonig-dev libxml2-dev \
    libcurl4-openssl-dev pkg-config libssl-dev libsqlite3-dev \
    && docker-php-ext-install pdo pdo_sqlite mysqli bcmath

RUN pecl install mongodb && docker-php-ext-enable mongodb

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

COPY . /var/www/html/

RUN chown -R www-data:www-data /var/www/html && chmod -R 755 /var/www/html

RUN printf '<Directory "/var/www/html">\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>\n' > /etc/apache2/conf-available/custom-access.conf && \
    a2enconf custom-access
