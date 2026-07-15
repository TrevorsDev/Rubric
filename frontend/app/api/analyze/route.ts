import { NextRequest, NextResponse } from "next/server";

const LAMBDA_URL =
  "https://aii3x6ter7.execute-api.us-east-1.amazonaws.com";

export async function POST(req: NextRequest) {
  const body = await req.json();

  const lambdaRes = await fetch(LAMBDA_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await lambdaRes.json();
  return NextResponse.json(data, { status: lambdaRes.status });
}
