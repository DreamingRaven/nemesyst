# @Author: George Onoufriou <archer>
# @Date:   2019-08-16
# @Email:  george raven community at pm dot me
# @Filename: debug_predictors.py
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root


def main(**kwargs):
    """Entry point called by Nemesyst, always yields dictionary, tuple or None.

    :param **kwargs: Generic input method to handle infinite dict-args.
    :rtype: yield dict
    """
    args = kwargs["args"]
    db = kwargs["db"]

    db.connect()

    # define a pipeline to get the latest gridfs file in any collection
    fs_pipeline = [{'$sort': {'uploadDate': -1}},  # sort most recent first
                   {'$limit': 1},  # we only want one model
                   {'$project': {'_id': 1}}]  # we only want its _id
    args["dl_output_model_collection"]
    # we add a suffix to target the metadata collection specifically
    # at the end of the top level model collection name we specified in our
    # config file
    model_coll_root = args["dl_output_model_collection"][args["process"]]
    model_coll_files = "{0}{1}".format(model_coll_root, ".files")
    # apply this pipeline to the collection we used to store the models
    fc = db.getCursor(db_collection_name=model_coll_files,
                      db_pipeline=fs_pipeline)
    # we could return several models but we have limited everything to only one
    # but to be extensible this shows how to get the models from the db
    # in batches, however since we only have one model a batch size higher than
    # one does nothing
    for batch in db.getFiles(db_batch_size=1, db_data_cursor=fc,
                             db_collection_name=model_coll_root):
        for doc in batch:
            # now read the gridout object to get the model (pickled)
            model = doc["gridout"].read()
            print(doc, type(model))

    yield None
