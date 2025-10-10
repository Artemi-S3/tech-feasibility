import { S3Client, ListBucketsCommand, PutObjectCommand, GetObjectCommand} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client();

const listBuckets = async () => {
  const out = await s3.send(new ListBucketsCommand({}));
  console.log(out.Buckets?.map(b => b.Name));
};

const uploadString = async (bucket, key, text) => {
  await s3.send(new PutObjectCommand({
    Bucket: bucket, 
    Key: key, 
    Body: body
  }));
};

const downloadToString = async (bucket, key) => {
  const out = await s3.send(new GetObjectCommand({
    Bucket: bucket, 
    Key: key
  }));
  const chunks = []
  for await (const chunk of out.Body) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
};

const presignGet = async (bucket, key, seconds = 300) => {
  return getSignedUrl(s3, new GetObjectCommand({
    Bucket: bucket, 
    Key: key
  }), { expiresIn: seconds });
};

const run = async () => {
  const bucket = "my-bucket";
  const key = "demo/hello-world.txt";
  await listBuckets();
  await uploadString(bucket, key, "hello from node");
  console.log(await downloadToString(bucket, key));
  console.log(await presignGet(bucket, key));
};

run().catch(console.error);
