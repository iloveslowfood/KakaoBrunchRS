import copy
import pandas as pd
import numpy as np


def squeeze(arr: list) -> list:
    """2차원 리스트를 1차원으로 squeeze

    Args:
        arr (list): 2차원 리스트. 각 원소는 int, float, list 중 하나의 자료형을 가짐

    Returns:
        list: 1차원 리스트. 각 원소는 int 또는 float
    """    
    result = []
    for l in arr:
        if len(l) > 0 and isinstance(l, list):
            result.extend(l)
        elif not isinstance(l, list):
            result.append(l)
    return result


def get_tfidf(data: pd.DataFrame, vocab: list, indices: list=None) -> pd.DataFrame:
    """tf-idf matrix를 리턴하는 함수. 서브샘플링을 통해 일부 데이터셋에 대해서만 tf-idf를 구할 수 있음
    tf-idf 방식
        - tf: boolean
        - idf: logarithmic
        - Reference: https://ko.wikipedia.org/wiki/Tf-idf
    Args:
        data (pd.DataFrame): 전체 데이터셋
        vocab (list): TF-IDF를 매길 태그 리스트
        indices (list, optional): 샘플링할 경우 활용. iloc에 사용될 인덱스 리스트를 입력(정수로 단일 샘플링도 가능). Defaults to None.

    Returns:
        pd.DataFrame: 사이즈가 (data size, vocab_size)인 TF-IDF matrix
    """    
    if isinstance(indices, int):
        indices = [indices]
    vocab_size = len(vocab)
    num_docs = data.shape[0]
    sample = copy.deepcopy(data) if indices is None else data.iloc[indices, :]
    output = pd.DataFrame(np.zeros((sample.shape[0], vocab_size)), columns=vocab)
    
    kwd_list = set(squeeze(sample['keyword_list'].tolist()))
    idf_vec = pd.DataFrame(np.zeros((1, vocab_size)), columns=vocab)
    for tag in kwd_list:
        idf_vec.loc[0, tag] = np.log(num_docs / sum(sample['keyword_list'].apply(lambda x: tag in x)))
    output = output.apply(lambda x: onehot(x, sample), axis=1) * idf_vec.values
    return output


def onehot(sample_row: pd.DataFrame, sample):
    """boolean-type TF를 구하는 함수. get_tfidf() 내부에서 다음과 같은 형태로 활용
           
        output.apply(lambda x: onehot(x, sample), axis=1)

    Args:
        sample_row (pd.Series): apply 함수가 적용된 샘플 데이터의 각 행
        sample (pd.DataFrame): 샘플 데이터. 키워드 리스트 정보를 얻기 위해 활용

    Returns:
        [type]: [description]
    """    
    idx = sample_row.name
    for tag in sample['keyword_list'].iloc[idx]:
        sample_row[tag] += 1
    return sample_row



# deprecated: 매우 느림
# def get_tfidf(data, vocab: list, indices: list=None, tf_type: str='boolean'):
#     if isinstance(indices, int):
#         indices = [indices]
#     vocab_size = len(vocab)
#     num_docs = data.shape[0]
#     sample = copy.deepcopy(data) if indices is None else data.iloc[indices, :]
#     output = pd.DataFrame(np.zeros((sample.shape[0], vocab_size)), columns=vocab)

#     if tf_type == 'boolean':
#         tf = 1 # boolean tf
#         output.apply(lambda )
#         for _, row in sample.iterrows():
#             tfidf = dict().fromkeys(vocab)
#             for tag in row['keyword_list']:
#                 idf = np.log(num_docs / sum(sample['keyword_list'].apply(lambda x: tag in x)))
#                 tfidf[tag] = tf * idf
#             output = output.append(tfidf, ignore_index=True)
#     else:
#         raise NotImplementedError()

#     return output