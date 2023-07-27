from src.unitxt.metrics import MetricPipeline, HuggingfaceMetric
from src.unitxt.test_utils.metrics import test_metric
from src.unitxt import add_to_catalog
from src.unitxt.blocks import CastFields, CopyPasteFields
import numpy as np
import evaluate

# metric = evaluate.load("sacrebleu")
# def get_sentence_bleu(metric, pred, gold):
    # score = metric.compute(predictions=[pred], references=[[gold]])['score']
    # return score

# if __name__ == "__main__":

#     predictions = ["hello there general kenobi", "on our way to ankh morpork"]
#     references = [["hello there general kenobi", "hello there !"], ["goodbye ankh morpork", "ankh morpork"]]

#     metric = evaluate.load("sacrebleu")
#     results = metric.compute(predictions=[predictions[1]], references=[references[1]]) #['score']
    
metric = MetricPipeline(
    main_score='score',
    preprocess_steps=[
        # CopyPasteFields(mapping=[('references/0', 'references')], use_dpath=True),
        # CastFields(
        #     fields={'prediction': 'float', 'references': 'float'}, 
        #     failure_defaults={'prediction': 0.0}, 
        #     use_dpath=True,
        # ),
    ],
    metric=HuggingfaceMetric(
        metric_name='sacrebleu',
        main_score='score',
        scale=100.0,
    )
)


predictions = ["hello there general kenobi", "on our way to ankh morpork"]
references = [["hello there general kenobi", "hello there !"], ["goodbye ankh morpork", "ankh morpork"]]

instance_targets = [{'score': 1.0, 'counts': [4, 3, 2, 1], 'totals': [4, 3, 2, 1], 'precisions': [100.0, 100.0, 100.0, 100.0], 'bp': 0.01, 'sys_len': 4, 'ref_len': 4},
                    {'score': 0.16, 'counts': [2, 1, 0, 0], 'totals': [6, 5, 4, 3], 'precisions': [33.33, 20.0, 12.5, 8.33], 'bp': 0.01, 'sys_len': 6, 'ref_len': 3}]
global_target = {'score': 0.4, 'counts': [6, 4, 2, 1], 'totals': [10, 8, 6, 4], 'precisions': [60.0, 50.0, 33.33, 25.0], 'bp': 0.01, 'sys_len': 10, 'ref_len': 7}


outputs = test_metric(
    metric=metric, 
    predictions=predictions, 
    references=references, 
    instance_targets=instance_targets, 
    global_target=global_target,
)

add_to_catalog(metric, 'metrics.bleu', overwrite=True)
