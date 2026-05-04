
import time
import json
import urllib.request

API_KEY = "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"
BASE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

MODELS = [
    "meta/llama-3.3-70b-instruct",
    "meta/llama-3.1-405b-instruct",
    "nvidia/llama-3.1-nemotron-70b-instruct",
    "deepseek-ai/deepseek-v3",
    "microsoft/phi-3.5-moe-16b-instruct"
]

def test_model(model_name):
    print(f"\n--- Probando: {model_name} ---")
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Hola, ¿cómo estás? Responde en una sola frase corta."}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    start_time = time.time()
    try:
        req = urllib.request.Request(BASE_URL, data=json.dumps(data).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            res_data = json.loads(response.read().decode())
            latency = time.time() - start_time
            content = res_data['choices'][0]['message']['content']
            print(f"Respuesta: {content}")
            print(f"Latencia: {latency:.2f} segundos")
            return latency, True
    except Exception as e:
        print(f"Error: {e}")
        return 0, False

results = []
for model in MODELS:
    latency, success = test_model(model)
    if success:
        results.append((model, latency))

print("\n\n=== RESULTADOS DEL BENCHMARK NVIDIA ===")
for model, latency in sorted(results, key=lambda x: x[1]):
    print(f"- {model}: {latency:.2f}s")
