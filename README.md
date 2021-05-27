# create_cname_records

simple Pulumi script to add some CNAME records to Akamai EdgeDNS.
We're using a reference to other pulumi project/stack to read the results from creating these CNAME records.

As it are two seperate stacks this one can be removed once the certificates have been approved by LetsEncrypt.
