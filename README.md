# That's the 'bath-house-bot', babe!

That's a simple telegram bot used by my friends inside our internal chat

It's a kind of pet project created as a joke, to avoid boring and simplify some routines, but then my friends often asked me to make some improvements and add some features, so I posted the project to GitHub and was going to invite them to collaborate around it.

Another issue here - I made deployments to my RaspberryPI not so often and even could forget credentials to it, or just lost details related to the deployment process - so solving that I've configured deploying to AWS Lambda using GitHub Actions CI and made the bot available via AWS API GateWay by REST and telegram web-hooks.

... I don't expect that's interesting for you, but these notes are mainly for me, like a kind of memory notes.

## ok, so how does it work now?

GitHub has been chosen as a source code storage, version control system and CI.
It has 2 branches: master and dev.
All pushes trigger the Actions CI that deploys the bot code to AWS and updates there the existing lambda function and it's layer with dependencies.
The Lambda has been created and configured before, it's been defined as available via AWS API Gateway for Telegram web-hooks by REST API.

So, if you'd like to contribute - just prepare your code in PR, merge it and if you didn't break anything then your code will update the bath-house-bot automatically. ENJOY! ;)

## Here's disclaimers and conventions for participants, and also technical details those I wouldn't like to forget later:

- the lambda code source file and the actual lambda handler function have to stay constant because the GitHub Action Deploy plugin expect that they should be named only as 'lambda_fubction.py' and 'lambda_handler' accordingly. Also, these names hardcoded (configured) inside AWS. So please don't rename it!
- the lambda python dependency management is very tricky, all of them should be provided inside an additional layer with the strict structure inside - the current actions deploy plugin do it well now, please don't broke that
- AWS subscription will expire somewhere in a year about, somewhere after July 2023, please keep that in mind and do something to prolong it or create and configure the new one
- don't keep sensitive data in code;
- to register Telegram web-hooks - you could use the [URL template](https://api.telegram.org/bot{your_bot_api_token}/setWebhook?url={your_api_gateway_url})
- ohh, of course, the code here provided as is and nobody has responsibilities for any issues or damage it affected.

## What's in TODO:

- add some tests and configure the testing flow - it's a bit of shame have no tests for QA/SDET ;)
- add currency exchange rates handler to the bot
- add the TODO list management feature - we have an internal joke about the List and the honor to keep it by somebody among us
- refactor the code - never had time for that %)
- ....

put some text here....later

pip freeze > requirements.txt


### P.S.: Here's a bunch of sources about simple telegram bots, AWS lambdas, GitHub, it's Actions CI and ideas that allow integrating all those staff:
- creating CI for Python projects using GitHubActions+AwsLambdas [Modern CI/CD Pipeline: Github Actions with AWS Lambda Serverless Python Functions and API Gateway
](https://towardsdatascience.com/modern-ci-cd-pipeline-git-actions-with-aws-lambda-serverless-python-functions-and-api-gateway-9ef20b3ef64a);
- the same, but in TouTube [AWS API Gateway to Lambda Tutorial in Python | Build a REST API](https://www.youtube.com/watch?v=uFsaiEhr1zs)
- a simple telegram bot (even not 'echo') in AWS Lambda with almost no additional libraries, so no lambda layers needed [Building A Simple Telegram Bot With AWS Lambda](https://medium.com/@toanphatdang/building-a-simple-telegram-bot-with-aws-lambda-c3143e596b3b)
- no CI, but a good example of ASYNC echo Telegram bot on AIOGRAM framework using AWS API Gateway & Lambda. [Aiogram AWS serverless example](https://github.com/DavisDmitry/aiogram-aws-serverless-example)
- another one basic AIOGRAM echo bot not in AWS, but in Heroku [Асинхронный телеграм-бот с вебхуками на Heroku](https://habr.com/ru/post/655965/)  
- again, no CI, but one more Echo bot with almost no dependencies [Serverless Telegram bot on AWS Lambda](https://medium.com/hackernoon/serverless-telegram-bot-on-aws-lambda-851204d4236c)
- the same, but another source [AWS Lambda And Telegram Bots: A Perfect Match](https://smyachenkov.com/posts/aws-lambda-telegram/) and [project in GitHup](https://github.com/smyachenkov/telegram-echo-bot-aws/blob/master/lambda_function.py)
- [Building a Telegram Bot with AWS API Gateway and AWS Lambda](https://chatbotslife.com/building-a-telegram-bot-with-aws-api-gateway-and-aws-lambda-21ef3239a053)
- some docs from AWS about Python Lambdas [Lambda function handler in Python](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)
- Actions library marketplace from GitHub [Actions](https://github.com/marketplace?type=actions&query=lambda+)
- Deploy code to Lambda [denzalman/lambda-python-action@v1.1.0](https://github.com/marketplace/actions/aws-lambda-python-deploy)
- this Action Plugin allows installing and configuring Python and run Python scripts inside Actions CI runner [actions/setup-python@v4](https://github.com/marketplace/actions/setup-python)
