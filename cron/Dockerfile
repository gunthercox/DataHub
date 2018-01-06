FROM alpine:latest

RUN apk --no-cache add curl

COPY ./job.sh /etc/periodic/15min/job
RUN chmod +x /etc/periodic/15min/job

CMD ["crond", "-fS"]
