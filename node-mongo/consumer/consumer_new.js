import { Kafka } from 'kafkajs';

const kafka = new Kafka({
    clientIds: 'node-server',
    brokers: ['localhost:29092']
})

const consumer = kafka.consumer({ groupId : 'kafka' })

export const run = async () => {

    await consumer.connect();

    await consumer.subscribe({ topics: ['comments'] })

    await consumer.run({
        eachMessage: async ({ topic, message}) => {
            let value = JSON.parse(message.value.toString())
            console.log({
                value: value.text,
                topic: topic
            })
        },
    })

}