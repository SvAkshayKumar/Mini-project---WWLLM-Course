import React, { useState, useEffect } from 'react';
import Header from './components/Header.jsx';
import Sidebar from './components/Sidebar.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Transliteration from './pages/Transliteration.jsx';
import Improvement from './pages/Improvement.jsx';
import Translation from './pages/Translation.jsx';
import KnowledgeBase from './pages/KnowledgeBase.jsx';
import Evaluation from './pages/Evaluation.jsx';
import SystemStatus from './pages/SystemStatus.jsx';

export default function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('indicwrite_theme') || 'light';
  });

  const [stats, setStats] = useState({
    transliterations: 14,
    improvements: 9,
    translations: 8
  });

  const [recentActivity, setRecentActivity] = useState([
    {
      type: 'transliteration',
      input: 'Namaste, aap kaise hain?',
      output: 'नमस्ते, आप कैसे हैं?',
      language: 'HI',
      time: '12:45 PM'
    },
    {
      type: 'improvement',
      input: 'हम जाएगा और काम करेगा',
      output: 'हम जाएंगे और काम करेंगे',
      language: 'HI (Grammar)',
      time: '12:40 PM'
    },
    {
      type: 'translation',
      input: 'Hello, how are you?',
      output: 'ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?',
      language: 'EN -> KN',
      time: '12:32 PM'
    }
  ]);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('indicwrite_theme', theme);
  }, [theme]);

  function toggleTheme() {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  }

  function handleLogActivity(item) {
    setRecentActivity(prev => [item, ...prev.slice(0, 19)]);
    setStats(prev => {
      const copy = { ...prev };
      if (item.type === 'transliteration') copy.transliterations += 1;
      if (item.type === 'improvement') copy.improvements += 1;
      if (item.type === 'translation') copy.translations += 1;
      return copy;
    });
  }

  return (
    <div className="app-container">
      <Sidebar
        currentTab={currentTab}
        onNavigate={setCurrentTab}
      />

      <div className="main-wrapper">
        <Header
          currentTab={currentTab}
          theme={theme}
          onToggleTheme={toggleTheme}
          onNavigate={setCurrentTab}
        />

        <main>
          {currentTab === 'dashboard' && (
            <Dashboard
              onNavigate={setCurrentTab}
              stats={stats}
              recentActivity={recentActivity}
            />
          )}

          {currentTab === 'transliteration' && (
            <Transliteration
              onLogActivity={handleLogActivity}
            />
          )}

          {currentTab === 'improvement' && (
            <Improvement
              onLogActivity={handleLogActivity}
            />
          )}

          {currentTab === 'translation' && (
            <Translation
              onLogActivity={handleLogActivity}
            />
          )}

          {currentTab === 'knowledge' && (
            <KnowledgeBase />
          )}

          {currentTab === 'evaluation' && (
            <Evaluation />
          )}

          {currentTab === 'settings' && (
            <SystemStatus />
          )}
        </main>
      </div>
    </div>
  );
}
