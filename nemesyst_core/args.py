# @Author: archer
# @Date:   2019-12-31T14:46:43+00:00
# @Last modified by:   archer
# @Last modified time: 2020-02-05T16:04:31+00:00

from future.utils import raise_
import os
import json
import configargparse


def argument_parser(description=None, cfg_files=None):
    """Parse cli>environment>config>default arguments into dictionary."""
    home = os.path.expanduser("~")
    parser = configargparse.ArgumentParser(prog=None,
                                           description=description,
                                           add_help=False,
                                           default_config_files=cfg_files)
    nemesyst = parser.add_argument_group(title="Nemesyst options")
    data = parser.add_argument_group(title="Data pre-processing options")
    deeplearning = parser.add_argument_group(title="Deep learning options")
    infering = parser.add_argument_group(title="Infering options")
    mongodb_rep = parser.add_argument_group(title="MongoDb replica options")
    mongodb_tls = parser.add_argument_group(title="MongoDb TLS options")
    mongodb = parser.add_argument_group(title="MongoDb options")

    # Nemesyst specific options
    nemesyst.add_argument("-h", "--help",
                          action="help",
                          env_var="N_HELP",
                          help="Print help.")
    nemesyst.add_argument("-U", "--update",
                          default=bool(False),
                          action="store_true",
                          env_var="N_UPDATE",
                          help="Nemesyst update, and restart.")
    nemesyst.add_argument("--prevent-update",
                          default=bool(False),
                          action="store_true",
                          env_var="N_PREVENT_UPDATE",
                          help="Prevent nemesyst from updating.")
    nemesyst.add_argument("-c", "--config",
                          default=list(),
                          nargs='+',
                          type=type_file_path_exists,
                          env_var="N_CONFIG",
                          help="List of all ini files to be used.")
    nemesyst.add_argument("--process-pool",
                          default=1,
                          type=int,
                          env_var="N_PROCESS_POOL",
                          help="The maximum number of processes to allocate.")

    # data pre-processing specific options
    data.add_argument("-d", "--data",
                      default=list(),
                      nargs='+',
                      type=type_file_path_exists,
                      env_var="N_DATA",
                      help="List of data file paths.")
    data.add_argument("--data-clean",
                      default=bool(False),
                      action="store_true",
                      env_var="N_DATA_CLEAN",
                      help="Clean specified data files.")
    data.add_argument("--data-cleaner",
                      default=[],
                      nargs='+',
                      type=type_file_path_exists,
                      env_var="N_DATA_CLEANER",
                      help="Path to data cleaner(s).")
    data.add_argument("--data-cleaner-entry-point",
                      default=["main"],
                      nargs='+',
                      type=str,
                      env_var="N_DATA_CLEANER_ENTRY_POINT",
                      help="Specify the entry point of custom scripts to use.")
    data.add_argument("--data-collection",
                      default=["debug_data"],
                      nargs='+',
                      type=str,
                      env_var="N_DATA_COLLECTION",
                      help="Specify data storage collection name(s).")

    # deep learning options
    deeplearning.add_argument("--dl-batch-size",
                              default=[32],
                              nargs='+',
                              type=int,
                              env_var="N_DL_BATCH_SIZE",
                              help="Batch size of the data to use.")
    deeplearning.add_argument("--dl-epochs",
                              default=[1],
                              nargs='+',
                              type=int,
                              env_var="N_DL_EPOCHS",
                              help="Number of epochs to train on data.")
    deeplearning.add_argument("--dl-learn",
                              default=bool(False),
                              action="store_true",
                              env_var="N_DL_LEARN",
                              help="Use learner scripts.")
    deeplearning.add_argument("--dl-learner",
                              default=[],
                              nargs='+',
                              type=type_file_path_exists,
                              env_var="N_DL_LEARNER",
                              help="Path to learner(s).")
    deeplearning.add_argument("--dl-learner-entry-point",
                              default=["main"],
                              nargs='+',
                              type=str,
                              env_var="N_DL_LEARNER_ENTRY_POINT",
                              help="Specify the entry point " +
                                   "of custom scripts to use.")
    deeplearning.add_argument("--dl-data-collection",
                              default=["debug_data"],
                              nargs='+',
                              type=str,
                              env_var="N_DL_DATA_COLLECTION",
                              help="Specify data collection name(s).")
    deeplearning.add_argument("--dl-data-pipeline",
                              default=[{}],
                              nargs='+',
                              type=str,
                              env_var="N_DL_DATA_PIPELINE",
                              help="Specify pipeline(s) for data retrieval.")
    deeplearning.add_argument("--dl-input-model-collection",
                              default=["debug_models"],
                              nargs='+',
                              type=str,
                              env_var="N_DL_INPUT_MODEL_COLLECTION",
                              help="Specify model storage collection to " +
                                   "retrain from.")
    deeplearning.add_argument("--dl-input-model-pipeline",
                              default=[{}],
                              nargs='+',
                              type=str,
                              env_var="N_DL_INPUT_MODEL_PIPELINE",
                              help="Specify model storage collection to " +
                                   "retrain from.")
    deeplearning.add_argument("--dl-output-model-collection",
                              default=["debug_models"],
                              nargs='+',
                              type=str,
                              env_var="N_DL_OUTPUT_MODEL_COLLECTION",
                              help="Specify model storage collection to " +
                                   "post trained neural networks to.")
    deeplearning.add_argument("--dl-sequence-length",
                              default=[32],
                              nargs='+',
                              type=int,
                              env_var="N_DL_SEQUENCE_LENGTH",
                              help="List of ints for how long a sequence of" +
                                   "data should be/ expected.")

    # Inference specific options
    infering.add_argument("--i-predictor",
                          default=[],
                          nargs='+',
                          type=type_file_path_exists,
                          env_var="N_I_PREDICTOR",
                          help="Path to predictor(s).")
    infering.add_argument("--i-predictor-entry-point",
                          default=["main"],
                          nargs='+',
                          type=str,
                          env_var="N_I_PREDICTOR_ENTRY_POINT",
                          help="Specify the entry point " +
                          "of predictor custom scripts to use.")
    infering.add_argument("--i-output-prediction-collection",
                          default=["debug_predictions"],
                          nargs='+',
                          type=str,
                          env_var="N_I_OUTPUT_PREDICTOR_COLLECTION",
                          help="Specify prediction storage collection to " +
                          "post trained neural network predictions to.")
    infering.add_argument("--i-predict",
                          default=bool(False),
                          action="store_true",
                          env_var="N_I_PREDICT",
                          help="Use predictor/ inferer scripts.")

    # MongoDB replica set options
    mongodb_rep.add_argument("--db-replica-set-name",
                             default=None,
                             type=str,
                             env_var="N_DB_REPLICA_SET_NAME",
                             help="Set the name for the replica set to use.")
    mongodb_rep.add_argument("--db-replica-read-preference",
                             default="primary",
                             type=str,
                             env_var="N_DB_REPLICA_READ_PREFERENCE",
                             help="Set the read preference of mongo client.")
    mongodb_rep.add_argument("--db-replica-max-staleness",
                             default=-1,
                             type=int,
                             env_var="N_DB_REPLICA_MAX_STALENESS",
                             help="Max seconds replica can be out of sync.")

    # MongoDB TLS options
    mongodb_tls.add_argument("--db-tls",
                             default=False,
                             action="store_true",
                             env_var="N_DB_TLS",
                             help="Set connection to mongodb use TLS.")
    mongodb_tls.add_argument("--db-tls-ca-file",
                             default=None,
                             type=type_file_path_exists,
                             env_var="N_DB_TLS_CA_FILE",
                             help="Certificat-authority certificate path.")
    mongodb_tls.add_argument("--db-tls-certificate-key-file",
                             default=None,
                             type=type_file_path_exists,
                             env_var="N_DB_TLS_CERTIFICATE_KEY_FILE",
                             help="Clients certificate and key pem path.")
    mongodb_tls.add_argument("--db-tls-certificate-key-file-password",
                             default=None,
                             type=str,
                             env_var="N_DB_TLS_CERTIFICATE_KEY_FILE_PASSWORD",
                             help="Set pass if certkey file needs password.")
    mongodb_tls.add_argument("--db-tls-crl-file",
                             default=None,
                             type=type_file_path_exists,
                             env_var="N_DB_TLS_CRL_FILE",
                             help="Path to certificate revocation list file.")

    # MongoDB specific options
    mongodb.add_argument("-l", "--db-login",
                         default=bool(False),
                         action="store_true",
                         env_var="N_DB_LOGIN",
                         help="Nemesyst log into mongodb.")
    mongodb.add_argument("-s", "--db-start",
                         default=bool(False),
                         action="store_true",
                         env_var="N_DB_START",
                         help="Nemesyst launch mongodb.")
    mongodb.add_argument("-S", "--db-stop",
                         default=bool(False),
                         action="store_true",
                         env_var="N_DB_STOP",
                         help="Nemesyst stop mongodb.")
    mongodb.add_argument("-i", "--db-init",
                         default=bool(False),
                         action="store_true",
                         env_var="N_DB_INIT",
                         help="Nemesyst initialise mongodb files.")
    mongodb.add_argument("--db-user-name",
                         type=str,
                         env_var="N_DB_USER_NAME",
                         help="Set mongodb username.")
    mongodb.add_argument("--db-password",
                         default=bool(False),
                         action="store_true",
                         env_var="N_DB_PASSWORD",
                         help="Set mongodb password.")
    mongodb.add_argument("--db-intervention",
                         default=bool(False),
                         action="store_true",
                         env_var="N_DB_INTERVENTION",
                         help="Manual intervention during database setup.")
    mongodb.add_argument("--db-authentication",
                         default=str("SCRAM-SHA-1"),
                         type=str,
                         env_var="N_DB_AUTHENTICATION",
                         help="Set the mongodb authentication method.")
    mongodb.add_argument("--db-authentication-database",
                         default=None,
                         type=str,
                         env_var="N_DB_AUTHENTICATION_DATABASE",
                         help="Override db_name as database to authenticate.")
    mongodb.add_argument("--db-user-role",
                         default=str("readWrite"),
                         type=str,
                         env_var="N_DB_USER_ROLE",
                         help="Set the users permissions in the database.")
    mongodb.add_argument("--db-ip",
                         default=str("localhost"),
                         type=str,
                         env_var="N_DB_IP",
                         help="The ip of the database to connect to.")
    mongodb.add_argument("--db-bind-ip",
                         default=["localhost"],
                         nargs='+',
                         type=str,
                         env_var="N_DB_BIND_IP",
                         help="The ip the database should be accessible from.")
    mongodb.add_argument("--db-port",
                         default=str("65535"),
                         type=str,
                         env_var="N_DB_PORT",
                         help="The port both the unauth and auth db will use.")
    mongodb.add_argument("--db-name",
                         default=str("nemesyst"),
                         type=str,
                         env_var="N_DB_NAME",
                         help="The name of the authenticated database.")
    mongodb.add_argument("--db-collection-name",
                         default=str("test"),
                         type=str,
                         env_var="N_DB_COLLECTION_NAME",
                         help="The name of the collection to use in database.")
    mongodb.add_argument("--db-config-path",
                         default=None,
                         type=type_path,
                         env_var="N_DB_CONFIG_PATH",
                         help="The path to the mongodb configuration file.")
    mongodb.add_argument("--db-path",
                         default=os.path.join(home, "db"),
                         type=type_path,
                         env_var="N_DB_PATH",
                         help="The parent directory to use for the database.")
    mongodb.add_argument("--db-log-path",
                         default=os.path.join(home, "db/log"),
                         type=type_path,
                         env_var="N_DB_PATH",
                         help="The parent directory to use for the db log.")
    mongodb.add_argument("--db-log-name",
                         default=str("mongo_log"),
                         type=str,
                         env_var="N_DB_LOG_NAME",
                         help="The base name of the log file to maintain.")
    mongodb.add_argument("--db-cursor-timeout",
                         default=600000,
                         type=int,
                         env_var="N_DB_CURSOR_TIMEOUT",
                         help="The duration in seconds before an unused " +
                              "cursor will time out.")
    mongodb.add_argument("--db-batch-size",
                         default=32,
                         type=int,
                         env_var="N_DB_BATCH_SIZE",
                         help="The number of documents to return from the " +
                              "db at once/ pre round.")
    mongodb.add_argument("--db-pipeline",
                         type=str,
                         env_var="N_DB_PIPELINE",
                         help="The file path of the pipeline to use on db.")

    return parser


argument_parser.__annotations__ = {"description": str,
                                   "cfg_files": list,
                                   "return": any}


def type_path(string):
    """Create a path from string."""
    return os.path.abspath(string)


type_path.__annotations__ = {"string": str, "return": str}


def type_file_path_exists(string):
    """Cross platform file path existance parser."""
    string = os.path.abspath(string)
    if os.path.isfile(string):
        return string
    else:
        # raise_(FileNotFoundError, str(string) + " does not exist.")
        raise_(ValueError, str(string) + " does not exist.")


type_file_path_exists.__annotations__ = {"string": str, "return": str}


def type_pipeline_file_path(string):
    """Cross platform json data loader."""
    fp = type_file_path_exists(string)
    with open(fp) as f:
        return json.load(f)


type_pipeline_file_path.__annotations__ = {"string": str, "return": str}
