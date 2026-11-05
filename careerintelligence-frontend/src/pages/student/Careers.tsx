import CareerCard from "../../components/CareerCard";
import { careers } from "../../data/mockData";

export default function Careers() {
  return (
    <div className="page">
      <div className="page-header"><div><span className="eyebrow">CAREER INTELLIGENCE</span><h1>Career paths</h1><p>Explore careers based on your academic and skills profile.</p></div></div>
      <div className="filter-bar"><input placeholder="Search careers..." /><select defaultValue="all"><option value="all">All demand levels</option><option>High</option><option>Growing</option><option>Stable</option></select></div>
      <div className="cards-grid three">{careers.map(career => <CareerCard key={career.id} career={career} />)}</div>
    </div>
  );
}