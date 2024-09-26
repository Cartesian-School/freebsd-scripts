#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to clear the screen
void display_clean() {
    system("clear");
    printf("\n");
}

// Function to run a system command and handle errors
void run_command(const char *command) {
    int ret = system(command);
    if (ret != 0) {
        printf("Command failed: %s\n", command);
        exit(1);
    }
}

// Function to check if Nginx is installed
int check_nginx_installed() {
    int ret = system("pkg info nginx >/dev/null 2>&1");
    if (ret == 0) {
        char reinstall_choice[10];
        printf("Nginx is already installed on this system.\n");
        while (1) {
            printf("Do you want to reinstall Nginx? (y/n): ");
            scanf("%s", reinstall_choice);
            if (strcmp(reinstall_choice, "y") == 0 || strcmp(reinstall_choice, "Y") == 0) {
                run_command("pkg remove -y nginx");
                run_command("pkg install -y nginx");
                return 1;
            } else if (strcmp(reinstall_choice, "n") == 0 || strcmp(reinstall_choice, "N") == 0) {
                printf("Nginx reinstallation canceled.\n");
                return 0;
            } else {
                printf("Invalid input. Please enter 'y' for yes or 'n' for no.\n");
            }
        }
    }
    return 1;
}

// Function to check Nginx status and start it if it's not running
void start_nginx_if_not_running() {
    int ret = system("service nginx status >/dev/null 2>&1");
    if (ret == 0) {
        printf("Nginx is already running.\n");
    } else {
        printf("Starting Nginx...\n");
        run_command("service nginx start");
    }
}

// Function to install Nginx
void install_nginx() {
    printf("Installing Nginx HTTP Server...\n");
    run_command("pkg install -y nginx");
    run_command("sysrc nginx_enable=YES");
    start_nginx_if_not_running();
}

// Function to configure Nginx as an HTTP/Proxy server
void configure_nginx() {
    const char *nginx_conf = "/usr/local/etc/nginx/nginx.conf";
    printf("Configuring Nginx as HTTP/Proxy server...\n");

    // Create a backup of the original configuration file
    run_command("cp /usr/local/etc/nginx/nginx.conf /usr/local/etc/nginx/nginx.conf.bak");

    // Write new configuration to the nginx.conf file
    FILE *f = fopen(nginx_conf, "w");
    if (f == NULL) {
        printf("Failed to open %s for writing.\n", nginx_conf);
        exit(1);
    }

    fprintf(f,
            "user  www;\n"
            "worker_processes  auto;\n"
            "error_log  /var/log/nginx/error.log warn;\n"
            "pid        /var/run/nginx.pid;\n\n"
            "events {\n"
            "    worker_connections  1024;\n"
            "}\n\n"
            "http {\n"
            "    include       mime.types;\n"
            "    default_type  application/octet-stream;\n\n"
            "    log_format  main  '$remote_addr - $remote_user [$time_local] \"$request\" '\n"
            "                      '$status $body_bytes_sent \"$http_referer\" '\n"
            "                      '\"$http_user_agent\" \"$http_x_forwarded_for\"';\n\n"
            "    access_log  /var/log/nginx/access.log  main;\n\n"
            "    sendfile        on;\n"
            "    keepalive_timeout  65;\n\n"
            "    server {\n"
            "        listen       80;\n"
            "        server_name  localhost;\n\n"
            "        location / {\n"
            "            root   /usr/local/www/nginx;\n"
            "            index  index.html index.htm;\n"
            "        }\n\n"
            "        error_page  500 502 503 504  /50x.html;\n"
            "        location = /50x.html {\n"
            "            root   /usr/local/www/nginx-dist;\n"
            "        }\n"
            "    }\n\n"
            "    server {\n"
            "        listen 8080;\n"
            "        location / {\n"
            "            proxy_pass http://127.0.0.1:80;\n"
            "            proxy_set_header Host $host;\n"
            "            proxy_set_header X-Real-IP $remote_addr;\n"
            "            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n"
            "            proxy_set_header X-Forwarded-Proto $scheme;\n"
            "        }\n"
            "    }\n"
            "}\n");

    fclose(f);
    printf("Nginx configuration updated.\n");

    // Restart Nginx to apply the new configuration
    run_command("service nginx restart");
}

int main() {
    display_clean();

    printf("This script will install and configure Nginx as an HTTP and Proxy server.\n");

    // Check if Nginx is installed
    if (check_nginx_installed()) {
        printf("Proceeding with the installation and configuration of Nginx.\n");

        // Install Nginx
        install_nginx();

        // Configure Nginx
        configure_nginx();

        printf("\n"
               "             ,        ,\n"
               "            /(        )`\n"
               "            \\ \\___   / |\n"
               "            /- _  `-/  '\n"
               "           (/\\/ \\ \\   /\\\n"
               "           / /   | `    \\\n"
               "           O O   ) /    |\n"
               "           `-^--'`<     '\n"
               "          (_.)  _  )   /\n"
               "           `.___/   /\n"
               "             `-----' /\n"
               "        <----.     __\\ \n"
               "        <----|====O)))==)\n"
               "        <----'    `--'\n"
               "             `-----'\n"
               "     \n");

        printf("Nginx installation and configuration completed.\n");
    } else {
        printf("Nginx installation is not required.\n");
    }

    return 0;
}

// Run:
// 1.  cc -o install_nginx_http_proxy install_nginx_http_proxy.c
// 2   sudo ./install_nginx_http_proxy
