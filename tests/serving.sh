# creating basic non-config, non-replica, localhost, mongodb instance
nemesyst --db-init --db-start --db-login --db-stop \
         --db-user-name USERNAME --db-password \
         --db-path DBPATH --db-log-path DBPATH/LOGDIR
