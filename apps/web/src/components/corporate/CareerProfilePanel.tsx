"use client";

import type { CareerProfile, CorporateSector } from "@nexus/types";
import { Button, Input, Panel } from "@nexus/ui";
import { useEffect, useState } from "react";
import { MediaUploader } from "@/components/MediaUploader";
import {
  addWorkExperience,
  deleteWorkExperience,
  getCareerProfile,
  upsertCareerProfile,
} from "@/lib/api";
import { useTranslation } from "@/i18n";

export function CareerProfilePanel({
  token,
  sectors,
}: {
  token: string;
  sectors: CorporateSector[];
}) {
  const { t } = useTranslation();
  const [profile, setProfile] = useState<CareerProfile | null>(null);
  const [headline, setHeadline] = useState("");
  const [summary, setSummary] = useState("");
  const [skills, setSkills] = useState("");
  const [location, setLocation] = useState("");
  const [sectorFocus, setSectorFocus] = useState("general");
  const [openToWork, setOpenToWork] = useState(true);
  const [expCompany, setExpCompany] = useState("");
  const [expTitle, setExpTitle] = useState("");
  const [expStart, setExpStart] = useState("");
  const [expEnd, setExpEnd] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState<string | null>(null);

  async function load() {
    const p = await getCareerProfile(token);
    setProfile(p);
    setHeadline(p.headline ?? "");
    setSummary(p.summary ?? "");
    setSkills(p.skills ?? "");
    setLocation(p.location ?? "");
    setSectorFocus(p.sector_focus ?? "general");
    setOpenToWork(p.open_to_work);
  }

  useEffect(() => {
    load().catch(() => setProfile(null));
  }, [token]);

  async function save() {
    setLoading(true);
    setMsg(null);
    try {
      const p = await upsertCareerProfile(token, {
        headline: headline.trim(),
        summary: summary.trim(),
        skills: skills.trim(),
        location: location.trim(),
        sector_focus: sectorFocus,
        open_to_work: openToWork,
      });
      setProfile(p);
      setMsg(t("career.profileSaved"));
    } catch (e) {
      setMsg(e instanceof Error ? e.message : t("errors.generic"));
    } finally {
      setLoading(false);
    }
  }

  async function addExp() {
    if (!expCompany.trim() || !expTitle.trim()) return;
    setLoading(true);
    try {
      await addWorkExperience(token, {
        company: expCompany.trim(),
        title: expTitle.trim(),
        start_year: expStart || undefined,
        end_year: expEnd || undefined,
        is_current: !expEnd,
      });
      setExpCompany("");
      setExpTitle("");
      setExpStart("");
      setExpEnd("");
      await load();
      setMsg(t("career.experienceAdded"));
    } finally {
      setLoading(false);
    }
  }

  const score = profile?.profile_score ?? 0;

  return (
    <div className="space-y-4">
      <div className="rounded-xl border border-[#4FC3F7]/30 bg-gradient-to-br from-[#4FC3F7]/10 to-transparent p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-[10px] uppercase tracking-widest text-[#4FC3F7]">{t("career.nexCareer")}</p>
            <p className="text-sm font-medium text-[#F5F5F5]">{profile?.display_name}</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] text-[#5A5A5A]">{t("career.profileStrength")}</p>
            <p className="text-2xl font-bold text-[#4FC3F7]">{score}%</p>
          </div>
        </div>
        <div className="mt-2 h-1.5 rounded-full bg-[#1F1F1F] overflow-hidden">
          <div className="h-full bg-[#4FC3F7] transition-all" style={{ width: `${score}%` }} />
        </div>
      </div>

      <Panel open title={t("career.cvTitle")}>
        <MediaUploader
          context="cv"
          token={token}
          compact
          previewUrl={profile?.cv_url}
          onUploaded={async (m) => {
            const p = await upsertCareerProfile(token, { cv_url: m.url, cv_filename: m.original_name });
            setProfile(p);
            setMsg(t("career.cvUploaded"));
          }}
          onClear={async () => {
            const p = await upsertCareerProfile(token, { cv_url: "", cv_filename: "" });
            setProfile(p);
          }}
        />
        {profile?.cv_filename && (
          <p className="mt-2 text-[10px] text-[#8A8A8A]">📄 {profile.cv_filename}</p>
        )}
      </Panel>

      <Panel open title={t("career.aboutYou")}>
        <div className="space-y-3">
          <Input label={t("profile.headline")} value={headline} onChange={(e) => setHeadline(e.target.value)} placeholder={t("profile.headlinePlaceholder")} />
          <textarea
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
            placeholder={t("career.summaryPlaceholder")}
            rows={3}
            className="w-full rounded-md border border-[#2A2A2A] bg-[#0A0A0A] px-3 py-2 text-sm text-[#F5F5F5]"
          />
          <Input label={t("profile.skills")} value={skills} onChange={(e) => setSkills(e.target.value)} placeholder={t("profile.skillsPlaceholder")} />
          <Input label={t("career.location")} value={location} onChange={(e) => setLocation(e.target.value)} placeholder="London, UK" />
          <label className="block text-[10px] uppercase tracking-wider text-[#5A5A5A]">
            {t("corporate.sector")}
            <select
              value={sectorFocus}
              onChange={(e) => setSectorFocus(e.target.value)}
              className="mt-1 w-full rounded-md border border-[#2A2A2A] bg-[#0A0A0A] px-3 py-2 text-sm text-[#F5F5F5]"
            >
              {sectors.map((s) => (
                <option key={s.id} value={s.id}>{s.label}</option>
              ))}
            </select>
          </label>
          <label className="flex items-center gap-2 text-xs text-[#8A8A8A]">
            <input type="checkbox" checked={openToWork} onChange={(e) => setOpenToWork(e.target.checked)} className="accent-[#4FC3F7]" />
            {t("career.openToWork")}
          </label>
          <Button size="sm" loading={loading} onClick={save}>{t("profile.saveChanges")}</Button>
        </div>
      </Panel>

      <Panel open title={t("career.experience")}>
        <ul className="mb-3 space-y-2">
          {(profile?.experiences ?? []).map((e) => (
            <li key={e.id} className="flex justify-between border-b border-[#1F1F1F] py-2 text-xs">
              <div>
                <p className="text-[#F5F5F5] font-medium">{e.title} · {e.company}</p>
                <p className="text-[#5A5A5A]">{e.start_year}{e.end_year ? ` – ${e.end_year}` : " – present"}</p>
              </div>
              <button type="button" className="text-[#5A5A5A] hover:text-[#FF5252]" onClick={() => deleteWorkExperience(token, e.id).then(load)}>✕</button>
            </li>
          ))}
        </ul>
        <div className="grid grid-cols-2 gap-2">
          <Input value={expTitle} onChange={(e) => setExpTitle(e.target.value)} placeholder={t("career.role")} />
          <Input value={expCompany} onChange={(e) => setExpCompany(e.target.value)} placeholder={t("career.company")} />
          <Input value={expStart} onChange={(e) => setExpStart(e.target.value)} placeholder="2020" />
          <Input value={expEnd} onChange={(e) => setExpEnd(e.target.value)} placeholder={t("career.present")} />
        </div>
        <Button size="sm" className="mt-2" variant="secondary" loading={loading} onClick={addExp}>{t("career.addExperience")}</Button>
      </Panel>

      {msg && <p className="text-xs text-[#00E5FF]">{msg}</p>}
    </div>
  );
}