import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import LanguageSelector from './LanguageSelector';
import { Sprout, LayoutDashboard, Camera, History, BookOpen, Pill, User, Menu, X, LogIn, LogOut } from 'lucide-react';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const { t } = useLanguage();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { to: '/', label: t('nav.home', 'Home') },
    { to: '/detect', label: t('nav.detect', 'Diagnose Crop'), icon: Camera, highlight: true },
    { to: '/dashboard', label: t('nav.dashboard', 'Dashboard'), icon: LayoutDashboard },
    { to: '/history', label: t('nav.history', 'History'), icon: History },
    { to: '/treatments', label: t('nav.treatments', 'Treatments'), icon: Pill },
    { to: '/resources', label: t('nav.resources', 'Learning Center'), icon: BookOpen },
  ];

  const isActive = (path) => {
    if (path === '/' && location.pathname !== '/') return false;
    return location.pathname.startsWith(path);
  };

  return (
    <header className="sticky top-0 z-40 bg-emerald-900/95 backdrop-blur-md border-b border-emerald-800 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-emerald-700/80 group-hover:bg-emerald-600 flex items-center justify-center text-emerald-100 shadow-inner border border-emerald-500/30 transition-all">
              <Sprout className="w-6 h-6 text-emerald-300" />
            </div>
            <div>
              <span className="font-extrabold text-lg sm:text-xl tracking-tight text-white flex items-center gap-1.5">
                {t('app_name', 'AgriVision AI')}
                <span className="text-[10px] bg-emerald-700/80 text-emerald-200 uppercase px-1.5 py-0.5 rounded-sm font-semibold tracking-wide border border-emerald-600/50">TAH-015</span>
              </span>
              <p className="text-[11px] text-emerald-300/80 font-medium hidden sm:block leading-tight">
                {t('app_tagline', 'Precision Crop Disease Predictor')}
              </p>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden lg:flex items-center gap-1">
            {navLinks.map((link) => {
              const active = isActive(link.to);
              if (link.highlight) {
                return (
                  <Link
                    key={link.to}
                    to={link.to}
                    className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-semibold bg-emerald-500 hover:bg-emerald-400 text-stone-950 transition-all shadow-md shadow-emerald-500/20 active:scale-95 ml-1"
                  >
                    <Camera className="w-4 h-4 text-stone-950" />
                    <span>{link.label}</span>
                  </Link>
                );
              }
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`px-3 py-2 rounded-xl text-sm font-medium transition-colors ${
                    active
                      ? 'bg-emerald-800 text-white font-semibold'
                      : 'text-emerald-100/90 hover:bg-emerald-800/50 hover:text-white'
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>

          {/* Right Section: Language Selector + Auth Info */}
          <div className="flex items-center gap-2 sm:gap-3">
            <LanguageSelector />

            {isAuthenticated ? (
              <div className="hidden sm:flex items-center gap-2 pl-2 border-l border-emerald-800">
                <Link
                  to="/profile"
                  className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-800/80 hover:bg-emerald-800 border border-emerald-700/50 text-xs sm:text-sm font-medium transition-colors"
                >
                  <div className="w-6 h-6 rounded-full bg-emerald-600 flex items-center justify-center font-bold text-xs text-white">
                    {user?.full_name ? user.full_name[0].toUpperCase() : 'F'}
                  </div>
                  <span className="hidden md:inline max-w-[100px] truncate">{user?.full_name}</span>
                </Link>
                <button
                  onClick={logout}
                  title={t('nav.logout', 'Sign Out')}
                  className="p-2 rounded-xl bg-emerald-800/40 hover:bg-emerald-800 text-emerald-200 hover:text-white transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="hidden sm:flex items-center gap-2 pl-2 border-l border-emerald-800">
                <Link
                  to="/login"
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs sm:text-sm font-medium text-emerald-200 hover:text-white hover:bg-emerald-800/60 transition-colors"
                >
                  <LogIn className="w-4 h-4" />
                  <span>{t('nav.login', 'Sign In')}</span>
                </Link>
                <Link
                  to="/register"
                  className="hidden md:inline-flex items-center px-3 py-1.5 rounded-xl text-xs sm:text-sm font-medium bg-emerald-800 hover:bg-emerald-700 text-white border border-emerald-600/50 transition-colors"
                >
                  {t('nav.register', 'Register')}
                </Link>
              </div>
            )}

            {/* Mobile Hamburger Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-xl bg-emerald-800/80 text-emerald-100 hover:text-white focus:outline-hidden"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6 text-emerald-200" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-emerald-950 border-b border-emerald-800 px-4 pt-3 pb-5 space-y-1 animate-in slide-in-from-top-4 duration-150">
          {navLinks.map((link) => {
            const active = isActive(link.to);
            return (
              <Link
                key={link.to}
                to={link.to}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-base font-medium transition-colors ${
                  link.highlight
                    ? 'bg-emerald-500 text-stone-950 font-bold'
                    : (active ? 'bg-emerald-800 text-white' : 'text-emerald-100 hover:bg-emerald-900')
                }`}
              >
                {link.icon && <link.icon className="w-5 h-5" />}
                <span>{link.label}</span>
              </Link>
            );
          })}

          <div className="pt-3 border-t border-emerald-800/80 mt-3 flex items-center justify-between">
            {isAuthenticated ? (
              <div className="flex items-center justify-between w-full">
                <Link
                  to="/profile"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-2 text-sm font-medium text-emerald-200 hover:text-white"
                >
                  <User className="w-4 h-4 text-emerald-400" />
                  <span>{user?.full_name}</span>
                </Link>
                <button
                  onClick={() => {
                    logout();
                    setMobileMenuOpen(false);
                  }}
                  className="text-xs px-3 py-1.5 rounded-lg bg-emerald-900 text-emerald-300 hover:text-white"
                >
                  {t('nav.logout', 'Sign Out')}
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3 w-full">
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-1/2 text-center py-2 rounded-xl text-sm font-medium bg-emerald-900 text-emerald-100 hover:bg-emerald-800"
                >
                  {t('nav.login', 'Sign In')}
                </Link>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-1/2 text-center py-2 rounded-xl text-sm font-semibold bg-emerald-600 text-white hover:bg-emerald-500"
                >
                  {t('nav.register', 'Register')}
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
