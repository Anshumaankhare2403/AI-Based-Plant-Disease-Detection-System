import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import App from '../App';

describe('PlantCare AI - Frontend UI & Component Tests', () => {
  it('TC-017: Renders branding, hero header, and diagnosis CTA button', () => {
    render(<App />);
    const brandElements = screen.getAllByText(/PlantCare/i);
    expect(brandElements.length).toBeGreaterThan(0);
    expect(screen.getByRole('link', { name: /Diagnose Leaf Now/i })).toBeInTheDocument();
  });

  it('TC-018: Renders navigation bar links', () => {
    render(<App />);
    const homeLinks = screen.getAllByRole('link', { name: /Home/i });
    expect(homeLinks.length).toBeGreaterThan(0);
    const dashboardLinks = screen.getAllByRole('link', { name: /Dashboard/i });
    expect(dashboardLinks.length).toBeGreaterThan(0);
    const historyLinks = screen.getAllByRole('link', { name: /History/i });
    expect(historyLinks.length).toBeGreaterThan(0);
  });

  it('TC-019: Renders supported crops tags', () => {
    render(<App />);
    expect(screen.getByText(/Tomato/i)).toBeInTheDocument();
    expect(screen.getByText(/Potato/i)).toBeInTheDocument();
    expect(screen.getByText(/Corn/i)).toBeInTheDocument();
  });

  it('TC-020: Renders workflow pipeline steps', () => {
    render(<App />);
    expect(screen.getByText(/Upload Foliage Photo/i)).toBeInTheDocument();
    expect(screen.getByText(/Neural Feature Extraction/i)).toBeInTheDocument();
    expect(screen.getByText(/Actionable Pathology Plan/i)).toBeInTheDocument();
  });
});
