# ToDo

## Hot

- [ ] cfg by [flask](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)
- [ ] vacancy storage object (transparent: inmem/file/k-v/any):
  - manager (list, iterate, filter)
  - objects (? (AdDict)): load/save/init/update:bool/history
- save last refresh date (timestamp/unixtime)
- list filter != query filter
- Vac list:
  - save responses
  - add $
  - add real url
  - Store:
    - As is
  - Refresh =>
    - Show new
    - Handle deleted
  - Shrink details
  - chk state
  - add &cross;
- vac:
  - store history (git?)
- vac store: plain file / k-v / docDB (mongo), SQL+JSON (postgres, sqlite+json1 ext)

## Enhancements

- compact pager
- login/logout
- session

## Misc

- Dups: https://spb.hh.ru/vacancy/34597232 https://spb.hh.ru/vacancy/34461767

## Done

+ [x] load cfg
+ [x] save filter to ~~cookie~~ session
