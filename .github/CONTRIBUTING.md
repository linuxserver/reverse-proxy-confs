# Contributing to reverse-proxy-confs

## Gotchas

* While contributing make sure to make all your changes before creating a Pull Request
* Read, and fill the Pull Request template
  * If the PR is addressing an existing issue include, closes #\<issue number>, in the body of the PR commit message
* If you want to discuss changes, you can also bring it up in [#dev-talk](https://discordapp.com/channels/354974912613449730/757585807061155840) in our [Discord server](https://discord.gg/YWrKVTn)

### Styling

* Indentation: 4 spaces
* Line-endings: LF
* Trailing newline: yes

### Requirements

* Must have the date on the first line, in YYYY/MM/DD format
* For subdomains, add a comment for a needed CNAME
* If the application needs further configuration, specify this in a comment

* In most cases we want the comments for Authelia, ldap and basic auth to be present
* If the application has known API endpoints, we prefer these to be exempt from auth trough a location block (provided the application has security on the endpoint)

* Files must not be executeable
