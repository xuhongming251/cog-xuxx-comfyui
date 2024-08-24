# Local UI Test

- start comfyui
```
sudo cog run -p 8188 bash
```

```
cd ComfyUI/
```
```
python main.py --listen 0.0.0.0
```

- open link
```
http://localhost:8188/
```
- test api

```
python3 test_basic_api_example.py
```


# Local Predict Test

```
python3 test_local_predict_cmd.py
```

or use cmd below, it can print log realtime

```
cog predict -i workflow=test0

```

```
cog predict -i workflow=test1
```

# Step by Step

1. install wsl2
2. install ubuntu24.04 in wsl2
3. install docker
4. install cog in ubuntu
5. test env in local
   1. Test the local UI by the link http://localhost:8188/ to verify that the env of comfyui and the custom nodes work.
   
   >> del all local checkpoints models、local input images, and test below.

   2. by test_basic_api_example.py, verify the dev workflow api json file.
   3. by test_local_predict_cmd.py, test local predict cmd.
   4. the predict cmd, the model file automatically downloads by name.
   5. the predict cmd, inputting image parameters use http online address.
   6. the predict cmd, that the output directory images will return.

6. add github action for push model.
   1. need config secrets.REPLICATE_API_TOKEN use replicate api token.
   2. push action

7. Dos and Don'ts for Publishing
   1. Needs to be done 
      1. add custom_nodes pip deps in cog.yaml
      2. check the checkpoints name has been in weights.json
      3. change the input images in api flow json file, use http online address
      4. can add extra params in predict.py, predict fun
      5. config .dockerignore, add not static files like models file(will dynamic download) to dockerignore.

    2. Not necessary.
       1. 