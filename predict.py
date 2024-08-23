from cog import BasePredictor, Path, Input
 
class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        print("in setup") 
    def predict(self,
            image: Path = Input(description="Image"),
            scale: float = Input(description="Factor", default=1.5)
    ) -> Path:
        output = f"hello, {scale}"
        print(output)
        return Path("./test.png")
