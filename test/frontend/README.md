# Hacker News Analytics Dashboard - Frontend

A modern Next.js frontend for the Hacker News Analytics Dashboard with real-time charts and interactive story exploration.

## 🚀 Features

- **Dashboard**: Real-time analytics with charts and statistics
- **Story Explorer**: Searchable and filterable story table
- **Background Tasks**: Trigger and monitor data fetching tasks
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Live task status monitoring

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Tables**: TanStack Table
- **HTTP Client**: Axios

## 📦 Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set environment variables** (optional):
   Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## 🏃‍♂️ Running the Frontend

### Development Mode
```bash
npm run dev
```
The frontend will be available at [http://localhost:3000](http://localhost:3000)

### Production Build
```bash
npm run build
npm start
```

## 📱 Pages

### Dashboard (`/dashboard`)
- Overview statistics
- AI keyword frequency chart
- Domain distribution pie chart
- Recent stories list
- Background task controls

### Explorer (`/explorer`)
- Searchable story table
- Keyword and domain filtering
- Pagination
- Sortable columns

## 🔧 API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000` by default.

### Key API Endpoints Used:
- `GET /dashboard` - Dashboard data
- `GET /stories` - Story list with filtering
- `GET /analytics` - Keyword analytics
- `GET /domains` - Domain analytics
- `POST /tasks/fetch-stories/` - Trigger story fetching
- `GET /tasks/{task_id}` - Task status

## 🎨 Customization

### Styling
- Uses Tailwind CSS for styling
- Custom colors and components can be added in `tailwind.config.js`
- Component styles are in the respective component files

### Charts
- Charts are built with Recharts
- Easy to customize colors, sizes, and data display
- Responsive design built-in

### Tables
- Uses TanStack Table for advanced table features
- Supports sorting, filtering, and pagination
- Customizable columns and cell rendering

## 🚀 Deployment

### Vercel (Recommended)
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy automatically

### Other Platforms
The app can be deployed to any platform that supports Next.js:
- Netlify
- Railway
- DigitalOcean App Platform
- AWS Amplify

## 🔍 Development

### Project Structure
```
src/
├── app/                 # Next.js App Router pages
│   ├── dashboard/       # Dashboard page
│   ├── explorer/        # Explorer page
│   └── layout.tsx       # Root layout
├── components/          # Reusable components
│   └── Navigation.tsx   # Navigation component
└── lib/                 # Utilities and API client
    └── api.ts          # API client and types
```

### Adding New Features
1. Create new pages in `src/app/`
2. Add components in `src/components/`
3. Extend API client in `src/lib/api.ts`
4. Update navigation if needed

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Ensure the backend is running on `http://localhost:8000`
   - Check CORS settings in the backend
   - Verify API endpoints are working

2. **Build Errors**
   - Clear `.next` folder: `rm -rf .next`
   - Reinstall dependencies: `rm -rf node_modules && npm install`

3. **Chart Not Rendering**
   - Check if data is being fetched correctly
   - Verify chart data format matches expected structure

## 📄 License

This project is part of the Hacker News Analytics Dashboard.
