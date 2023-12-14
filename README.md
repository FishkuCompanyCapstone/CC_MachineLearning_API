<h1>ML API Docs</h1>

Endpoint:

[**Machine Learning**](#machine-learning)

- [Cek Kesegaran Ikan](#fish-freshness)
- [Klasifikasi Ikan](#fish-classification)

## Machine Learning

### Cek Kesegaran Ikan

- Endpoint
  - /freshness
- Method
  - POST
- Request form-data

  - photo_url = img file format (.jpg .png .tif .jpeg)
  - fish_name = string

- Response

```json
{
  "prediction": "highly_fresh"
}
```

### Klasifikasi Ikan

- Endpoint
  - /classify
- Method
  - POST
- Request form-data
  - photo_url = img file format (.jpg .png .tif .jpeg)
- Response

```json
{
  "fish_name": "kuniran"
}
```
