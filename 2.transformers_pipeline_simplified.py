from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

class Pipeline(ABC):

    def __init__(
        self
    ):
        pass

    @abstractmethod
    def preprocess(self, input_, **preprocess_parameters: Dict):
        raise NotImplementedError("preprocess not implemented")

    @abstractmethod
    def _forward(self, input_tensors, **forward_parameters: Dict):
        raise NotImplementedError("_forward not implemented")

    @abstractmethod
    def postprocess(self, model_outputs, **postprocess_parameters: Dict):
        raise NotImplementedError("postprocess not implemented")

    def forward(self, model_inputs, **forward_params):
        with self.device_placement():
            if self.framework == "tf":
                model_inputs["training"] = False
                model_outputs = self._forward(model_inputs, **forward_params)
            elif self.framework == "pt":
                inference_context = self.get_inference_context()
                with inference_context():
                    model_inputs = self._ensure_tensor_on_device(model_inputs, device=self.device)
                    model_outputs = self._forward(model_inputs, **forward_params)
            else:
                raise ValueError(f"Framework {self.framework} is not supported")
        return model_outputs
    
    def __call__(self, inputs, *args, num_workers=None, 
        batch_size=None, **kwargs):
        preprocess_params = ...
        forward_params = ...
        postprocess_params = ...
        return self.run_single(inputs, 
            preprocess_params, 
            forward_params, 
            postprocess_params)

    def run_single(self, inputs, preprocess_params, 
                forward_params, postprocess_params):
        model_inputs = self.preprocess(inputs, **preprocess_params)
        model_outputs = self.forward(model_inputs, **forward_params)
        outputs = self.postprocess(model_outputs, **postprocess_params)
        return outputs


class TextClassificationPipeline(Pipeline):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, *args, **kwargs):
        result = super().__call__(*args, **kwargs)
        _legacy = "top_k" not in kwargs
        if isinstance(args[0], str) and _legacy:
            return [result]
        else:
            return result

    def preprocess(self, inputs, **tokenizer_kwargs):
        return self.tokenizer(inputs, 
            return_tensors=..., **tokenizer_kwargs)

    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs, 
        function_to_apply=None, top_k=1, _legacy=True):
        scores = model_outputs[0]

        dict_scores = [
            {"label": self.model.config.id2label[i]
            , "score": score.item()}
             for i, score in enumerate(scores)
        ]
        if not _legacy:
            dict_scores.sort(key=lambda x: x["score"], reverse=True)
            if top_k is not None:
                dict_scores = dict_scores[:top_k]
        return dict_scores


def pipeline(
    task: str = None,
    model = None,
    config = None,
    tokenizer = None,
    feature_extractor = None,
    image_processor = None,
    framework: Optional[str] = None,
    revision: Optional[str] = None,
    use_fast: bool = True,
    use_auth_token: Optional[Union[str, bool]] = None,
    device = None,
    device_map=None,
    torch_dtype=None,
    trust_remote_code: Optional[bool] = None,
    model_kwargs: Dict[str, Any] = None,
    pipeline_class: Optional[Any] = None,
    **kwargs,
) -> Pipeline:
    """
    Utility factory method to build a pipeline.
    """
    
    ...

    # 创建Pipeline对象
    return pipeline_class(
        model=model, 
        framework=framework, 
        task=task, **kwargs)