from pycaret.utils import enable_colab
from pycaret.datasets import get_data
from pycaret.classification import *
import pandas
from pycaret.nlp import *

data = pandas.read_csv('dataset.csv', error_bad_lines=False, encoding="ISO-8859-1")
data = data.sample(1000, random_state=786).reset_index(drop=True)
print(data.shape)
print(data)

exp_nlp101 = setup(data=data, target='text', session_id=344)
text_list = list(data['text'])
type(text_list)

exp_nlp101_list = setup(data=text_list, session_id=123)
lda2 = create_model('lda', num_topics=6, multi_core=True)
print(lda2)
lda_results = assign_model(lda2)
evaluate_model(lda2)
save_model(lda2, 'First')

lda_results['target'] = data['target']
lda_results.head()

pce_1 = setup(data=lda_results, target='target', session_id=5)
second = create_model('et')
evaluate_model(second)
save_model(second, 'Second')

data_for_testing = {
    'text': ['I want to die']
}
new_data = pandas.DataFrame(data_for_testing, columns=['text'])

dataset = get_topics(data=new_data, text='text', model=lda2)
