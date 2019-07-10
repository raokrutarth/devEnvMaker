# Analytics

Contains the big data application (compute + backend) and temprary storage

## Storage

- No persistant storage
- **Batch** computing on spark cluster
- Application self times the batch job
- Application streams DB onto Spark
- Submits Spark computation job
- Consistantly exposes latest report via REST
- Admin and increase/decrease batch job frequency
- Persistant DB restricts access to PI queries by analytics Application

## Future work

- Analytica application times batch job when Business layer/persistant DB is not busy
- Business layer dumps to pushes to Kafa strem ingested by spark
- Analytics layer presents the results of the streamed computation

## Data Generation

- Predicting Sales rep is filing farudulent expense report
- each datagenerator commits farud based on location/timing/their performance
- Predicting sales of a rep with regression
- identifying better paths
- plotting customer complaints in sales rep territory

## Refrences

- jupyter + docker: <https://jupyter-docker-stacks.readthedocs.io/en/latest/>
- list of similar projects: <https://github.com/search?q=docker-spark>
- kafka + spark + docker: <https://blog.antlypls.com/blog/2015/10/05/getting-started-with-spark-streaming-using-docker/>
- full big data demo app and code: <https://github.com/big-data-europe/demo-spark-sensor-data>
- <https://github.com/big-data-europe/docker-spark>
- <https://towardsdatascience.com/a-journey-into-big-data-with-apache-spark-part-1-5dfcc2bccdd2>
- <https://www.youtube.com/watch?v=Qei5VAnCpDM>
- <https://www.youtube.com/watch?v=z_D5L9h6B6c>
- <https://github.com/gettyimages/docker-spark>
- <https://github.com/carbonblack/docker-spark>
- <https://www.smaato.com/blog/spark-docker-amazon-ec2-code-tells-you-everything/>
