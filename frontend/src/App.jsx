import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';

import Navbar from './components/Navbar';
import Footer from './components/Footer';

import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import DiseaseDetectionPage from './pages/DiseaseDetectionPage';
import DiagnosisResultPage from './pages/DiagnosisResultPage';
import TreatmentsPage from './pages/TreatmentsPage';
import HistoryPage from './pages/HistoryPage';
import EducationalResourcesPage from './pages/EducationalResourcesPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';

export default function App() {
  return (
    <BrowserRouter>
      <LanguageProvider>
        <AuthProvider>
          <div className="flex flex-col min-h-screen">
            <Navbar />
            <main className="grow">
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/detect" element={<DiseaseDetectionPage />} />
                <Route path="/diagnosis/:id" element={<DiagnosisResultPage />} />
                <Route path="/treatments" element={<TreatmentsPage />} />
                <Route path="/history" element={<HistoryPage />} />
                <Route path="/resources" element={<EducationalResourcesPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </AuthProvider>
      </LanguageProvider>
    </BrowserRouter>
  );
}
