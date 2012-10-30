# Observatory

Observatory is a flask app that helps keep track of what versions of your
webapp are deployed in what environments.

## What now?

Observatory watches your Github repository and deployed environments and
figures out what versions are deployed where. First it checks your tagged
releases. Then it assumes you have the branches `master` and `stage`, which
represent the next two versions of your application. It also assumes that your
application is simply versioned with a single number (i.e. `v4`).

It exposes this information through an API so it can be consumed by other
tools. It presents it as an HTML page in a human readable form. The page
provides some additional features to aid in project management.
