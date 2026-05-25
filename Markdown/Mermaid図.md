```mermaid
flowchart TD
    A[開始] --> B[ログイン画面]
    B --> C{認証OK?}
    C -->|Yes| D[ダッシュボード]
    C -->|No| E[エラー表示]
    E --> B
```