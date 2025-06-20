Place this folder anywhere on your local machine. Before uploading, compress
the directory into a single archive, for example:

```bash
zip -r dataset_config.zip sol_project
```

Send this zip file to `/api/v1/dataset/{id}/config`. Each image then needs to be
uploaded separately via `/api/v1/dataset/{id}/image`. The `val.json` file
**must** exist even if it is empty.
