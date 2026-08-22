/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    const backendUrl =
      process.env.RAILWAY_API_URL ||
      process.env.NEXT_PUBLIC_API_URL ||
      'https://sunami47-ai-data-bridge.hf.space';
    return [
      {
        source: '/api/backend/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
      {
        source: '/api/health',
        destination: `${backendUrl}/health`,
      },
    ];
  },
};

module.exports = nextConfig;
