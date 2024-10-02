## Known bugs and issues

### LLM
- [ ] Sometimes run_query_tool is invoked before describe_table_tool. This makes the query to use incorrect table schema
- [ ] run_query_tool does not use % for wildcard search

### Available slot fetching logic
- [ ] fetch tennismesta slot miss slots having a few hours in between. For example if the court is free from 19-22, only 19 and 22 are shown as available slots. 20 and 21 are not shown as available slots.