import { sign, verify, decode } from "jsonwebtoken";

const jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJzY3JpYmVkIjpmYWxzZSwiaWF0IjoxNzI3NDkzMzk2LCJleHAiOjE3Mjc0OTY5OTZ9.Xs-A26nl1fqsZTfyMiVrIMSFSMB6OwglhubRIydw-rU";

const data = decode(jwt);

data["subscribed"] = true

console.log("sign", sign(data, ));
