# An example of how to convert a given API workflow into its own Replicate model
# Replace predict.py with this file when building your own workflow

import os
import mimetypes
import json
import shutil
from typing import List
from cog import BasePredictor, Input, Path
from comfyui import ComfyUI
from cog_model_helpers import optimise_images
from cog_model_helpers import seed as seed_helper

OUTPUT_DIR = "/tmp/outputs"
INPUT_DIR = "/tmp/inputs"
COMFYUI_TEMP_OUTPUT_DIR = "ComfyUI/temp"
ALL_DIRECTORIES = [OUTPUT_DIR, INPUT_DIR, COMFYUI_TEMP_OUTPUT_DIR]

mimetypes.add_type("image/webp", ".webp")

# Force HF offline
os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

test_flow0 = """
{
    "3": {
      "inputs": {
        "seed": 628176032045934,
        "steps": 20,
        "cfg": 8,
        "sampler_name": "euler",
        "scheduler": "normal",
        "denoise": 1,
        "model": [
          "4",
          0
        ],
        "positive": [
          "6",
          0
        ],
        "negative": [
          "7",
          0
        ],
        "latent_image": [
          "5",
          0
        ]
      },
      "class_type": "KSampler",
      "_meta": {
        "title": "KSampler"
      }
    },
    "4": {
      "inputs": {
        "ckpt_name": "majicmixRealistic_v7.safetensors"
      },
      "class_type": "CheckpointLoaderSimple",
      "_meta": {
        "title": "Load Checkpoint"
      }
    },
    "5": {
      "inputs": {
        "width": 512,
        "height": 512,
        "batch_size": 1
      },
      "class_type": "EmptyLatentImage",
      "_meta": {
        "title": "Empty Latent Image"
      }
    },
    "6": {
      "inputs": {
        "text": "beautiful scenery nature glass bottle landscape, , purple galaxy bottle,",
        "clip": [
          "4",
          1
        ]
      },
      "class_type": "CLIPTextEncode",
      "_meta": {
        "title": "CLIP Text Encode (Prompt)"
      }
    },
    "7": {
      "inputs": {
        "text": "text, watermark",
        "clip": [
          "4",
          1
        ]
      },
      "class_type": "CLIPTextEncode",
      "_meta": {
        "title": "CLIP Text Encode (Prompt)"
      }
    },
    "8": {
      "inputs": {
        "samples": [
          "3",
          0
        ],
        "vae": [
          "4",
          2
        ]
      },
      "class_type": "VAEDecode",
      "_meta": {
        "title": "VAE Decode"
      }
    },
    "9": {
      "inputs": {
        "filename_prefix": "ComfyUI",
        "images": [
          "8",
          0
        ]
      },
      "class_type": "SaveImage",
      "_meta": {
        "title": "Save Image"
      }
    }
  }
"""

test_flow1 = """
{
  "10": {
    "inputs": {
      "enabled": true,
      "swap_model": "inswapper_128.onnx",
      "facedetection": "retinaface_resnet50",
      "face_restore_model": "GFPGANv1.4.pth",
      "face_restore_visibility": 1,
      "codeformer_weight": 0.5,
      "detect_gender_input": "no",
      "detect_gender_source": "no",
      "input_faces_index": "0",
      "source_faces_index": "0",
      "console_log_level": 1,
      "input_image": [
        "11",
        0
      ],
      "source_image": [
        "12",
        0
      ]
    },
    "class_type": "ReActorFaceSwap",
    "_meta": {
      "title": "ReActor 🌌 Fast Face Swap"
    }
  },
  "11": {
    "inputs": {
      "image": "https://xuwx.oss-cn-shenzhen.aliyuncs.com/yyy.jpeg",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "12": {
    "inputs": {
      "image": "https://xuwx.oss-cn-shenzhen.aliyuncs.com/huge.webp",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "13": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "10",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}
"""
class Predictor(BasePredictor):
    def setup(self):
        self.comfyUI = ComfyUI("127.0.0.1:8188")
        self.comfyUI.start_server(OUTPUT_DIR, INPUT_DIR)

    def predict(
        self,
        workflow: str = Input(
            default="",
        ),
        output_format: str = optimise_images.predict_output_format(),
        output_quality: int = optimise_images.predict_output_quality(),
        force_reset_cache: bool = Input(
            description="Force reset the ComfyUI cache before running the workflow. Useful for debugging.",
            default=False,
        ),
    ) -> List[Path]:
        
        self.comfyUI.cleanup(ALL_DIRECTORIES)

        self.comfyUI.connect()
        
        if force_reset_cache:
            self.comfyUI.reset_execution_cache()

        if workflow == "test0":
            workflow = test_flow0

        if workflow == "test1":
            workflow = test_flow1

        flow = self.comfyUI.load_workflow(workflow)

        self.comfyUI.run_workflow(flow)
        
        output_directories = [OUTPUT_DIR]

        ret_img_list = optimise_images.optimise_image_files(
            output_format, output_quality, self.comfyUI.get_files(output_directories)
        )

        # print(ret_img_list)

        return ret_img_list
