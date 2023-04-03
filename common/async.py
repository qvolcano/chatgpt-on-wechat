def async_run(co):
  loop = asyncio.get_event_loop()
  get_future = asyncio.ensure_future(co) # 相当于开启一个future
  loop.run_until_complete(get_future) # 事件循环
  return get_future.result()
