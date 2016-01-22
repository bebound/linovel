## Contribution

Free free to report bug and send Pull-Request.

It's also very easy to let linovel support more website by add a new rule.

Here is some rule about creating a new rule:

- Create a `novel_xxx.py` with website domain.
- In `novel_xxx.py`, create a class inherit from `AbstractNovel`
- `check_url`,`extract_novel_information`,`get_novel_information` are 3 most important method need to override. More detailed information can be found in `novel.py`