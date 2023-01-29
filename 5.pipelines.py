from abc import ABC, abstractmethod
import random
from typing import List,Union

class Pipeline(ABC):
    @abstractmethod
    def call(self, *args, **kwargs) -> Union[str, List[str]]:
        ...
    
    def __call__(self,*args, **kwargs) -> Union[str, List[str]]:
        print("Model is predicting.....")
        return self.call(*args, **kwargs)

class ClassificationPipeline(Pipeline):

    def call(self, sentences):
        if isinstance(sentences, str):
            sentences = [sentences]
        return ["positive" if random.random()<0.5 else "negative" for sent in sentences]


class TextGenerationPipeline(Pipeline):
    def call(self, prompt):
        if not isinstance(prompt, str):
            raise ValueError("prompt shoule be a string")
        return prompt + "I wrote something else here."


PIPELINE_ROUTER = {
    "sentiment-classification":ClassificationPipeline,
    "text-generation":TextGenerationPipeline
}

def pipeline(task, *args, **kwargs) -> Pipeline:
    if not task in PIPELINE_ROUTER.keys():
        raise ValueError(f"known task {task}")
    return PIPELINE_ROUTER[task](*args, **kwargs)

if __name__ == "__main__":
    sentences = ["The weather is good today.", "I am unhappy."]

    clf_pipeline = ClassificationPipeline()
    preds = clf_pipeline(sentences)
    print(preds)


    gen_pipeline = TextGenerationPipeline()
    preds = gen_pipeline(sentences[0])
    print(preds)

    pipe = pipeline("sentiment-classification")
    print(pipe(sentences))

    pipe = pipeline("text-generation")
    print(pipe(sentences[0]))