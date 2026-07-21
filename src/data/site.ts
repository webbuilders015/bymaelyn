export const site = {
  name: 'Art of Beauty by Maelyn',
  tagline: 'Schoonheidsspecialist in Delft',
  description:
    'Schoonheidsspecialiste gespecialiseerd in huidverbeterende gezichtsbehandelingen, chemische peelings, microdermabrasie, waxen en diverse andere schoonheidsbehandelingen.',
  url: 'https://bymaelyn.nl',
  address: {
    street: 'Bagijnhof 1',
    postalCode: '2611 AN',
    city: 'Delft',
    mapsUrl: 'https://goo.gl/maps/EfcWGj16SxnGjuNWA',
  },
  contact: {
    email: 'info@bymaelyn.nl',
    phone: '015-2155081',
    phoneHref: 'tel:015-2155081',
    whatsapp: '06-18664586',
    whatsappHref: 'https://wa.me/31618664586',
  },
  kvk: '84290609',
  btw: 'NL003950890B32',
  bookingUrl: 'https://art-of-beauty-by-maelyn.salonized.com/widget_bookings/new',
  social: {
    facebook: 'https://www.facebook.com/Artofbeautybymaelyn/',
    instagram: 'https://www.instagram.com/artofbeauty.bymaelyn/',
  },
  googleReviewUrl: 'https://www.google.com/maps/place/?q=place_id:ChIJyW8INPO1xUcRAAPBA2Z3s1E',
  anbosUrl: 'https://www.anbos.nl/consument/schoonheidsspecialist/kies-voor-gediplomeerd',
  openingHours: [
    { day: 'Maandag', hours: 'Gesloten' },
    { day: 'Dinsdag', hours: '09:00 - 18:00' },
    { day: 'Woensdag', hours: '09:00 - 18:00' },
    { day: 'Donderdag', hours: '12:00 - 21:00' },
    { day: 'Vrijdag', hours: '09:30 - 18:00' },
    { day: 'Zaterdag', hours: '08:30 - 16:00' },
    { day: 'Zondag', hours: 'Gesloten' },
  ],
  webshops: [
    { label: 'Skincare webshop', url: 'https://shop.bymaelyn.nl' },
    { label: 'Sieraden webshop', url: 'https://jewellery-bymae.nl/' },
  ],
  usps: [
    'Anbos gecertificeerde schoonheidsspecialiste',
    'Jarenlange ervaring',
    'Huidverbeterende gezichtsbehandelingen',
  ],
};

export const treatments = [
  {
    slug: 'gezichtsbehandeling',
    title: 'Gezichtsbehandeling',
    short: 'Huidverbeterende gezichtsbehandelingen op maat.',
    image: '/images/treatments/gezichtsbehandeling.jpg',
    icon: 'facial',
  },
  {
    slug: 'chemische-peeling',
    title: 'Chemische peeling',
    short: 'Professionele peelings voor een frisse, egale huid.',
    image: '/images/treatments/gezichtsbehandeling.jpg',
    icon: 'peeling',
  },
  {
    slug: 'microdermabrasie',
    title: 'Microdermabrasie',
    short: 'Mechanische peeling voor een directe glow en verfijnde poriën.',
    image: '/images/treatments/microdermabrasie.jpg',
    icon: 'microderm',
  },
  {
    slug: 'waxen',
    title: 'Waxen',
    short: 'Ontharen op de vakkundige en hygiënische manier.',
    image: '/images/treatments/waxen.webp',
    icon: 'wax',
  },
  {
    slug: 'wenkbrauwen-epileren',
    title: 'Wenkbrauwstyling',
    short: 'Wenkbrauwen epileren en in model brengen.',
    icon: 'brows',
    image: '/images/treatments/wenkbrauwen.webp',
  },
];

export const brands = [
  {
    slug: 'paulas-choice',
    title: "Paula's Choice",
    short: 'Wetenschappelijk onderbouwde huidverzorging.',
    logo: '/images/brands/paulas-choice.png',
  },
  {
    slug: 'skeyndor',
    title: 'Skeyndor',
    short: 'Professionele, huidverbeterende cosmetica.',
    logo: '/images/brands/skeyndor.png',
  },
];

export const mainNav = [
  {
    label: 'Webshops',
    href: '#',
    children: site.webshops.map((w) => ({ label: w.label, href: w.url })),
  },
  {
    label: 'Over mij',
    href: '/over-mij/',
  },
  {
    label: 'Behandelingen',
    href: '/behandelingen/',
    children: treatments.map((t) => ({ label: t.title, href: `/${t.slug}/` })),
  },
  {
    label: 'Merken',
    href: '/merken/',
    children: brands.map((b) => ({ label: b.title, href: `/${b.slug}/` })),
  },
  { label: 'Reviews', href: '/reviews/' },
  { label: 'Contact', href: '/contact/' },
];
