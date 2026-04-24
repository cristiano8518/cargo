# Testing Guide

## Unit + Integration Tests

Run all tests:

```powershell
py -3 manage.py test
```

Run tests with coverage:

```powershell
py -3 -m coverage run manage.py test
py -3 -m coverage report
```

## Load Testing (k6)

1. Start app locally:

```powershell
py -3 manage.py runserver
```

2. Run k6 scenario:

```powershell
k6 run .\load-tests\k6-smoke.js
```

Use custom target URL:

```powershell
k6 run -e BASE_URL=https://your-service.onrender.com .\load-tests\k6-smoke.js
```
