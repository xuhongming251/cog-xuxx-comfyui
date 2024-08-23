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
- or test in cmd

```
python3 test_basic_api_example.py
```


# Local Predict Test

```
python3 test_local_predict_cmd.py
```