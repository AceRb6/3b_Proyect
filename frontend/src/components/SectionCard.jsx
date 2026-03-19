export default function SectionCard({ title, actions, children }) {
  return (
    <section className="section-card">
      <div className="section-header">
        <div>
          <h3>{title}</h3>
        </div>
        {actions}
      </div>
      {children}
    </section>
  );
}
