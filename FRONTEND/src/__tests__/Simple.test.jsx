import { render, screen } from '@testing-library/react';

function SimpleComponent() {
  return <h1>Hello World</h1>;
}

test('renders hello world', () => {
  render(<SimpleComponent />);
  expect(screen.getByText('Hello World')).toBeInTheDocument();
});