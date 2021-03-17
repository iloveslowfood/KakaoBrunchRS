from dataclasses import dataclass

# data_root = "./raw"
# tfidf_root = '../raw/preprocessed/metadata_tfidf'
# vocab_root = '../raw/preprocessed/tag_vocab7000.csv'


@dataclass
class DataRoots:
    raw: str = "./raw"
    tfidf: str = (
        "preprocessed/metadata_tfidf/metadata_tfidf_vocab7000_aggregation.npz"
    )
    user_time_read: str = "preprocessed/user_time_read.json"
    vocab: str = "preprocessed/tag_vocab7000.csv"
    post_id_dec: str = "preprocessed/post_id_decoding.pickle"
    post_id_enc: str = "preprocessed/post_id_encoding.pickle"
