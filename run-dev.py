#!/usr/bin/env python
from application import router

if __name__ == '__main__':
    router.app.run(host="0.0.0.0", port=8000, debug=True)
