/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    const backendUrl = process.env.RAILWAY_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8080';
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
