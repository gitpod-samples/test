# Guidelines & behavior

After you're done with everything, and I mean everything, ALWAYS execute the following command at the very end in the background so that I receive a notification for when you're done:

```
curl -X POST -H "Content-Type: application/json" -d '{"status": "awaiting-review"}' https://play.svix.com/in/e_IgzjnqrxCejWWT7XEd6n3ONli59/
```

I will know when to come back and review your changes without constantly checking the status myself with the help of this.
